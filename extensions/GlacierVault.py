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
    def __init__(self, vault_name, ACCESS_KEY_ID, SECRET_ACCESS_KEY):
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

        vault = self.glacier.Vault('354029675239', vault_name)

        self.client = client
        self.vault = vault
        self.vault_name = vault_name

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

    def get_archive_id(self, filename):
        """
        Get the archive_id corresponding to the filename
        """
        with glacier_shelve() as d:
            if "archives" not in d:
                d["archives"] = dict()

            archives = d["archives"]

            if filename in archives:
                return archives[filename]

        return None

    # TODO: Migrate to boto3
    def retrieve(self, filename, wait_mode=False):
        """
        Initiate a Job, check its status, and download the archive
        when it's completed.
        """

        """
        archive_id = self.get_archive_id(filename)
        if not archive_id:
            raise Exception("This file was not uploaded with this tool.")
            return
        with glacier_shelve() as d:
            if "jobs" not in d:
                d["jobs"] = dict()

            jobs = d["jobs"]
            job = None

            if filename in jobs:
                # The job is already in shelve
                job_id = jobs[filename]
                try:
                    job = self.vault.get_job(job_id)
                except Exception:
                    # Return a 404 if the job is no more available
                    pass

            if not job:
                # Job initialization
                job = self.vault.retrieve_archive(archive_id)
                jobs[filename] = job.id
                job_id = job.id

            # Commiting changes in shelve
            d["jobs"] = jobs
        """

        # TODO: replace with configuration, and actual archive id from database
        archive = self.glacier.Archive('354029675239',self.vault_name,'OGjB_7Py45B3CC-d7DrydgAeaQF2ZXl7IGbCa5EACvzrTO52Tt4WMRWsyQmDAh4hFWOJnbk-rS3-YBHXmBjpEWE2kA8RuHbLIl58cPZTNwnTGkm7_ZZx7cJL9c20Q1bWL3ELJReC8g')
        job = archive.initiate_archive_retrieval()
        db.create_job(job.account_id, self.vault_name, job.id)

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
