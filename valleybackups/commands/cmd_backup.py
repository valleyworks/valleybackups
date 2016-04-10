import os
import click
from valleybackups import db
from valleybackups.config_context import pass_config
import hashlib
from os.path import isfile

@click.command()
@click.option('-f', '--force', is_flag=True)
@click.argument('file', type=click.File('r'))
@pass_config
def cli(config, force, file):
    """Store a file in a AWS Glacier Vault
    """
    filename = os.path.split(file.name)[1]   # Removes absolute path if there is one
    click.echo("Uploading file %s" % filename)
    
    if db.check_if_exists(hashlib.sha256(file.read()).hexdigest()) and force is False:
        click.echo("This file is already backed up.")
    else:
        try:
            if config.service == "Glacier":
                config.glacier.upload(file.name)
                click.echo("File %s uploaded." % filename)
        except Exception as e:
            click.echo("Error uploading file")
            click.echo(e.message)

