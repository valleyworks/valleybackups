import os
import boto3
import hashlib
from botocore.exceptions import ClientError
from valleybackups import db


class GlacierClient:
    """
    Wrapper for uploading/download archive to/from Amazon Glacier Vault.

    Parameters
    ----------
    VAULT_NAME : str
    ACCESS_KEY_ID : str
    SECRET_ACCESS_KEY : str
    AWS_ACCOUNT_ID : str
    """
    def __init__(self, VAULT_NAME, ACCESS_KEY_ID, SECRET_ACCESS_KEY, AWS_ACCOUNT_ID, REGION_NAME):
        client = boto3.client('glacier',
                              region_name=REGION_NAME,
                              aws_access_key_id=ACCESS_KEY_ID,
                              aws_secret_access_key=SECRET_ACCESS_KEY)

        self.glacier = boto3.resource('glacier',
                                      region_name=REGION_NAME,
                                      aws_access_key_id=ACCESS_KEY_ID,
                                      aws_secret_access_key=SECRET_ACCESS_KEY)

        # vault = self.glacier.Vault(AWS_ACCOUNT_ID, VAULT_NAME)

        self.client = client
        # self.vault = vault
        self.VAULT_NAME = VAULT_NAME
        self.AWS_ACCOUNT_ID = AWS_ACCOUNT_ID
        self.REGION_NAME = REGION_NAME
        self.ACCESS_KEY_ID = ACCESS_KEY_ID
        self.SECRET_ACCESS_KEY = SECRET_ACCESS_KEY

    def init_vault(self, AWS_ACCOUNT_ID, VAULT_NAME):
        """Initiates the Vault"""
        self.vault = self.glacier.Vault(AWS_ACCOUNT_ID, VAULT_NAME)

    def upload(self, filename):
        """Upload filename and store the archive id for future retrieval
    
        Parameters
        ----------
        filename: str
          Name of the file
        
        Returns
        -------
        boto3.Glacier.Archive
        """

        try:
            with open(filename, mode='rb') as file:  # b is important -> binary
                fileContent = file.read()
                try:
                    response = self.vault.upload_archive(
                        archiveDescription=filename,
                        body=fileContent
                    )

                    if response:
                        fileHash = hashlib.sha256(fileContent)
                        filename = os.path.split(filename)[1] # Removes absolute path if there is one
                        db.create_archive(filename, response.vault_name, response.id, fileHash.hexdigest())
                        return response

                except Exception, e:
                    raise Exception(e.response["Error"]["Message"])

        except Exception as e:
            raise

    def retrieve(self, archive_id):
        """
        Initiate a Job, check its status, and download the archive
        when it's completed.

        archive_id : str
        """

        archive = self.glacier.Archive(self.AWS_ACCOUNT_ID,self.VAULT_NAME,archive_id)
        job = archive.initiate_archive_retrieval()
        db.create_job(job.account_id, self.VAULT_NAME, job.id, job.status_code,archive_id)

        job_id = job
        print "Job %s: %s ( %s / %s )" % (job.action, job.status_code, str(job.creation_date), str(job.completion_date))
        print "Job ID: %s" % job.id

    # TODO: Refactor to download file in chunks
    def download_file(self, job_id):
        """
        Downloads a file which job has finished correctly

        job_id: str
        """

        job = self.glacier.Job(self.AWS_ACCOUNT_ID, self.VAULT_NAME, job_id)

        try:
            # Downloads the archive
            output = job.get_output()
        except ClientError as e:
            raise Exception(e.response["Error"]["Message"])

        # Gets file name
        archive_name = output["archiveDescription"]
        file_name = os.path.split(archive_name)[1] # Removes absolute path if there is one
        # Reads the file content
        file_body = output["body"].read()

        # Calculate hash tree
        import hashlib
        file_hash = hashlib.sha256(file_body)

        if file_hash.hexdigest() == job.sha256_tree_hash:
            print "Checksum OK"
            print "Writing file %s" % file_name
            with open(file_name, "wb") as f:
                f.write(file_body)
        else:
            print "Checksum ERROR"

    def create_vault(self, vault_name):
        """
            Creates a Vault
        """
        new_vault = self.glacier.create_vault(vaultName=vault_name)
        notification = self.glacier.Notification(self.AWS_ACCOUNT_ID, vault_name)

        sns = boto3.resource('sns',
                             region_name=self.REGION_NAME,
                             aws_access_key_id=self.ACCESS_KEY_ID,
                             aws_secret_access_key=self.SECRET_ACCESS_KEY)
        topic = sns.create_topic(Name='%sNotification' % vault_name)

        response = notification.set(
            vaultNotificationConfig={
                'SNSTopic': topic.arn,
                'Events': [
                    'ArchiveRetrievalCompleted',
                    'InventoryRetrievalCompleted',
                ]
            }
        )

        return True
