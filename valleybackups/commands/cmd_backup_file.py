import os
import click
from valleybackups.config import get_parser
from valleybackups.cli import pass_config

@click.command()
@click.argument('file', type=click.File('r'))
@pass_config
def cli(config, file):
    """Store a file in a AWS Glacier Vault
    """
    filename = os.path.split(file.name)[1] # Removes absolute path if there is one
    click.echo("Uploading file %s" % filename)
    
    if config.service == "Glacier":
      response = config.glacier.upload(file.name)

      if response:
          click.echo("File %s uploaded." % filename)
      else:
          click.echo("Error uploading file")