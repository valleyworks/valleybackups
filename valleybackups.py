import os
import click

from config import get_config
from extensions.glacier import GlacierClient
import db

class Config(object):
    def __init__(self):
        self.debug = False
        self.ACCESS_KEY_ID = get_config('base', 'ACCESS_KEY_ID')
        self.SECRET_ACCESS_KEY = get_config('base', 'SECRET_ACCESS_KEY')
        self.VAULT_NAME = get_config('glacier', 'VAULT_NAME')
        self.AWS_ACCOUNT_ID = get_config('base', 'AWS_ACCOUNT_ID')
        self.glacier = GlacierClient(self.VAULT_NAME,
                                self.ACCESS_KEY_ID,
                                self.SECRET_ACCESS_KEY,
                                self.AWS_ACCOUNT_ID)

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--debug', is_flag=True)
@pass_config
def cli(config, debug):
    config.debug = debug
    db.init(get_config('glacier', 'VAULT_NAME'), debug)

    pass

@cli.command()
@click.argument('file', type=click.File('r'))
@pass_config
def backup(config, file):
    """Store a file in a Glacier Vault
    """
    filename = os.path.split(file.name)[1] # Removes absolute path if there is one
    click.echo("Uploading file %s" % filename)
    
    response = config.glacier.upload(file.name)

    if response:
        click.echo("File %s uploaded." % filename)
    else:
        click.echo("Error uploading file")

@cli.command()
@pass_config
def list_files(config):
    """Outputs a list of backed up files
    """
    archives = db.get_files()
    print "ID - NAME"
    for archive in archives:
        print " %s - %s" % (archive.id, archive.name)

@cli.command()
def list_uncompleted_jobs():
    """Outputs uncompleted jobs to the console
    """
    jobs = db.get_uncompleted_jobs()
    print "ID - ARCHIVE"
    for job in jobs:
        print " %s - %s" % (job[0], job[1])

@cli.command()
@click.argument('archive_id', type=int)
@pass_config
def request_file(config, archive_id):
    """Requests a backup from Glacier
    """

    click.echo("Retrieving %s" % archive_id)

    glacier_archive_id = db.get_archive_id(archive_id)

    try:
        config.glacier.retrieve(glacier_archive_id)
    except Exception as e:
        click.echo(e)

@cli.command()
@click.argument('job_id', type=int)
def download_file(job_id):
    """Gets a ready-to-be-downloaded file from Glacier. """
    response = self.glacier.download_file(job_id)