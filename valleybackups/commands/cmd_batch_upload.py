from os import listdir
from os.path import isfile, join
import click
from valleybackups import db
from valleybackups.config import get_parser
from valleybackups.cli import pass_config
import hashlib

@click.command()
@click.option('-f', '--force', is_flag=True)
@click.argument('folder', type=click.Path(exists=True,dir_okay=True, resolve_path=True))
@pass_config
def cli(config, force, folder):
    """Store all files on folder to AWS Glacier
    """
    for file in listdir(folder):
        with open(join(folder, file), mode='rb') as open_file:
            checksum = hashlib.sha256(open_file.read()).hexdigest()
            print "Processing %s" % file
            if db.check_if_exists(checksum) and force is False:
                click.echo("This file is already backed up. Override with --force")  
                click.echo()
                    
            else:
                if config.service == "Glacier":
                    response = config.glacier.upload(open_file.name)

                if response:
                    click.echo("File %s uploaded." % file)
                else:
                    click.echo("Error uploading file")