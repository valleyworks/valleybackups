from pony.orm import *
import os

dbName = os.path.dirname(__file__) + "/database.sqlite"
db = Database("sqlite", dbName, create_db=True)


class Storage(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    type = Required(str)
    archives = Set("Archive")
    jobs = Set("Job")


class Archive(db.Entity):
    id = PrimaryKey(int, auto=True)
    storage = Required(Storage)
    name = Required(str)
    location = Required(str)
    checksum = Required(str)
    archiveId = Required(str)
    archive_parts = Set("ArchivePart")


class Job(db.Entity):
    id = PrimaryKey(int, auto=True)
    account_id = Required(str)
    job_id = Required(str)
    storage = Required(Storage)


class ArchivePart(db.Entity):
    id = PrimaryKey(int, auto=True)
    archive = Required(Archive)


def create_archive(name, vault_name, archiveId):
    with db_session:
        storage = Storage.get(name=vault_name)
        Archive(
            name=name,
            storage=storage,
            location=" ",
            checksum=" ",
            archiveId=archiveId)
        commit()
    # archive = Archive(storage=self.storage)

def create_job(account_id, vault_name, job_id):
    """Creates Job in DB
        This is needed to start the Retreival Job and track it.
    """
    with db_session:
        storage = Storage.get(name=vault_name)
        Job(
            account_id=account_id,
            storage=storage,
            job_id=job_id)
        commit()

def init(vault_name, debug):
    vault_name = vault_name

    if debug:
        sql_debug(True)
    db.generate_mapping(create_tables=True)

    with db_session:
        if count(s for s in Storage if s.name == vault_name) is 0:
            Storage(name=vault_name, type="Glacier")
            commit()
