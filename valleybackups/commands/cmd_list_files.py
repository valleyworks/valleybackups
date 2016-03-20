import click
from valleybackups import db
from valleybackups.cli import pass_config

@click.command()
@pass_config
def cli(config):
    """Outputs a list of backed up files
    """
    archives = db.get_files()
    print "ID - NAME - CREATED"
    for archive in archives:
        print " %s - %s - %s" % (archive.id, archive.name, archive.created_at)