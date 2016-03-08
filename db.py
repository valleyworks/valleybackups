from pony.orm import *
import os

dbName = os.path.dirname(__file__) + "/database.sqlite"
db = Database("sqlite", dbName, create_db=True)


class Storage(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    type = Required(str)
    archives = Set("Archive")


class Archive(db.Entity):
    id = PrimaryKey(int, auto=True)
    storage = Required(Storage)
    name = Required(str)
    location = Required(str)
    checksum = Required(str)
    archiveId = Required(str)
    archive_parts = Set("ArchivePart")


class ArchivePart(db.Entity):
    id = PrimaryKey(int, auto=True)
    archive = Required(Archive)


def create_archive(name, vault_name, data):
    with db_session:
        storage = Storage.get(name=vault_name)
        Archive(
            name=name,
            storage=storage,
            location=data["location"],
            checksum=data["checksum"],
            archiveId=data["archiveId"])
        commit()
    # archive = Archive(storage=self.storage)


def init(vault_name, debug):
    vault_name = vault_name

    if debug:
        sql_debug(True)
    db.generate_mapping(create_tables=True)

    with db_session:
        if count(s for s in Storage if s.name == vault_name) is 0:
            Storage(name=vault_name, type="Glacier")
            commit()
