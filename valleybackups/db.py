from pony.orm import *
from datetime import datetime
import os

dbName = os.path.dirname(__file__) + "/database.sqlite"
db = Database("sqlite", dbName, create_db=True)


class Storage(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    type = Required(str)
    archives = Set("Archive")
    jobs = Set("Job")
    created_at = Optional(datetime, default=datetime.now())


class Archive(db.Entity):
    id = PrimaryKey(int, auto=True)
    storage = Required(Storage)
    name = Required(str)
    location = Optional(str)
    checksum = Optional(str)
    archiveId = Required(str)
    archive_parts = Set("ArchivePart")
    jobs = Set("Job")
    created_at = Optional(datetime, default=datetime.now())



class Job(db.Entity):
    id = PrimaryKey(int, auto=True)
    account_id = Required(str)
    job_id = Required(str)
    storage = Required(Storage)
    status = Required(str)
    archive = Required(Archive)
    created_at = Optional(datetime, default=datetime.now())

class ArchivePart(db.Entity):
    id = PrimaryKey(int, auto=True)
    archive = Required(Archive)
    created_at = Optional(datetime, default=datetime.now())


def create_archive(name, vault_name, archiveId, checksum):
    with db_session:
        storage = Storage.get(name=vault_name)
        Archive(
            name=name,
            storage=storage,
            location=" ",
            checksum=checksum,
            archiveId=archiveId)
        commit()
    # archive = Archive(storage=self.storage)

@db_session
def create_job(account_id, vault_name, job_id, status_code, archive_id):
    """Creates Job in DB
        This is needed to start the Retreival Job and track it.
	account_id : str
	vault_name : str
	job_id : str
	status_code : str
	archive_id : str
    """
    with db_session:
        storage = Storage.get(name=vault_name)
	archive = Archive.get(archiveId=archive_id)
        Job(
            account_id=account_id,
            storage=storage,
            job_id=job_id,
            status=status_code,
	    archive=archive
	)
        commit()

@db_session
def update_job(job_id, status_code):
    """Updates job status
	job_id : str
	status_code : str
    """
    job = Job.get(job_id=job_id)
    job.status = status_code
    commit()

@db_session
def get_files():
    files = Archive.select()[:]
    return files

@db_session
def get_archive_id(id):
    return Archive.get(id=id).archiveId

@db_session
def get_uncompleted_jobs():
    """Returns uncompleted jobs
    These are file requests waiting for download
    """
    jobs = select((j.id, a.name) for j in Job for a in j.archive if j.status != "Succeeded")
    return jobs[:]

@db_session
def check_if_exists(checksum):
    """Check if the same has been uploaded before"""
    archive_count = count(a for a in Archive if a.checksum == checksum)
    if archive_count > 0:
        return True
    return False

def init_mapping():
    db.generate_mapping(create_tables=True)
    

def init(vault_name, debug):
    vault_name = vault_name

    if debug:
        sql_debug(True)

    init_mapping()

    with db_session:
        if count(s for s in Storage if s.name == vault_name) is 0:
            Storage(name=vault_name, type="Glacier")
            commit()
