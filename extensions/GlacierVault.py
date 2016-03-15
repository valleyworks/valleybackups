import boto3
from botocore.exceptions import ClientError
import shelve
import os
import db

SHELVE_FILE = os.path.expanduser("~/.valleybackups.db")


class glacier_shelve(object):
    """
    Context manager for shelve
    """

    def __enter__(self):
        self.shelve = shelve.open(SHELVE_FILE)
        return self.shelve

    def __exit__(self, exc_type, exc_value, traceback):
        self.shelve.close()


class GlacierVault:
    """
    Wrapper for uploading/download archive to/from Amazon Glacier Vault
    Makes use of shelve to store archive id corresponding to filename
    and waiting jobs.

    Backup:
    >>> GlacierVault("myvault")upload("myfile")

    Restore:
    >>> GlacierVault("myvault")retrieve("myfile")
    or to wait until the job is ready:
    >>> GlacierVault("myvault")retrieve("serverhealth2.py", True)
    """
    def __init__(self, VAULT_NAME, ACCESS_KEY_ID, SECRET_ACCESS_KEY, AWS_ACCOUNT_ID):
        """
        Initialize the vault
        """
        client = boto3.client('glacier',
                              region_name='us-west-2',
                              aws_access_key_id=ACCESS_KEY_ID,
                              aws_secret_access_key=SECRET_ACCESS_KEY)

        self.glacier = boto3.resource('glacier',
                                region_name='us-west-2',
                                aws_access_key_id=ACCESS_KEY_ID,
                                aws_secret_access_key=SECRET_ACCESS_KEY)

        vault = self.glacier.Vault(AWS_ACCOUNT_ID, VAULT_NAME)

        self.client = client
        self.vault = vault
        self.VAULT_NAME = VAULT_NAME
        self.AWS_ACCOUNT_ID = AWS_ACCOUNT_ID

    def upload(self, filename):
        """
        Upload filename and store the archive id for future retrieval
        """

        try:
            with open(filename, mode='rb') as file:  # b is important -> binary
                fileContent = file.read()

                response = self.vault.upload_archive(
                    archiveDescription=filename,
                    body=fileContent
                )

                if response:
                    db.create_archive(filename, response.vault_name, response.id)
                    return response

        except Exception as e:
            raise

    # TODO: Migrate to boto3
    def retrieve(self, filename, wait_mode=False):
        """
        Initiate a Job, check its status, and download the archive
        when it's completed.
        """

        # TODO: replace with configuration, and actual archive id from database
        archive = self.glacier.Archive(self.AWS_ACCOUNT_ID,self.VAULT_NAME,'OGjB_7Py45B3CC-d7DrydgAeaQF2ZXl7IGbCa5EACvzrTO52Tt4WMRWsyQmDAh4hFWOJnbk-rS3-YBHXmBjpEWE2kA8RuHbLIl58cPZTNwnTGkm7_ZZx7cJL9c20Q1bWL3ELJReC8g')
        job = archive.initiate_archive_retrieval()
        db.create_job(job.account_id, self.VAULT_NAME, job.id, job.status_code)

        # try:
        #     output = job.get_output()
        # except ClientError as e:
        #     raise

        job_id = job
        print "Job %s: %s ( %s / %s )" % (job.action, job.status_code, str(job.creation_date), str(job.completion_date))
        # checking manually if job is completed every 10 secondes instead of using Amazon SNS

        """
        if wait_mode:
            import time
            while 1:
                job = self.vault.get_job(job_id)
                if not job.completed:
                    time.sleep(10)
                else:
                    break

        if job.completed:
            print "Downloading..."
            job.download_to_file(filename)
        else:
            print "Not completed yet"
        """

    # TODO: Refactor to download file in chunks
    def download_file(self, job_id):
        """
        Downloads a file which job has finished correctly
        """
        job = self.glacier.Job(self.AWS_ACCOUNT_ID, self.VAULT_NAME, job_id)

        # Downloads the archive
        output = job.get_output()

        # Gets file name
        file_name = output["archiveDescription"]

        # Reads the file content
        file_body = output["body"].read()

        with open(file_name, "wb") as f:
            f.write(file_body)
