import boto3
from botocore.exceptions import ClientError
import os
import db


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
	VAULT_NAME : str
	ACCESS_KEY_ID : str
	SECRET_ACCESS_KEY : str
	AWS_ACCOUNT_ID : str
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

	filename: string
        """

        try:
            with open(filename, mode='rb') as file:  # b is important -> binary
                fileContent = file.read()

                response = self.vault.upload_archive(
                    archiveDescription=filename,
                    body=fileContent
                )

                if response:
		    import hashlib
                    fileHash = hashlib.sha256(fileContent)
                    db.create_archive(filename, response.vault_name, response.id, fileHash.hexdigest())
                    return response

        except Exception as e:
            raise

    def retrieve(self, archive_id, wait_mode=False):
        """
        Initiate a Job, check its status, and download the archive
        when it's completed.

	archive_id : str
	wait_mode : bool
        """

        # TODO: replace with configuration, and actual archive id from database
        archive = self.glacier.Archive(self.AWS_ACCOUNT_ID,self.VAULT_NAME,archive_id)
        job = archive.initiate_archive_retrieval()
        db.create_job(job.account_id, self.VAULT_NAME, job.id, job.status_code,archive_id)

        # try:
        #     output = job.get_output()
        # except ClientError as e:
        #     raise

        job_id = job
        print "Job %s: %s ( %s / %s )" % (job.action, job.status_code, str(job.creation_date), str(job.completion_date))
	print "Job ID: %s" % job.id
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

	job_id: str
        """
        job = self.glacier.Job(self.AWS_ACCOUNT_ID, self.VAULT_NAME, job_id)

        # Downloads the archive
        output = job.get_output()

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
            with open(file_name, "wb") as f:
                f.write(file_body)
	else:
	    print "Checksum ERROR"
