import click
from valleybackups import db
from valleybackups.cli import pass_config

@click.command()
@click.argument('archive_id', type=int)
@pass_config
def cli(config, archive_id):
    """Requests a backup from Glacier
    """

    click.echo("Retrieving %s" % archive_id)

    glacier_archive_id = db.get_archive_id(archive_id)

    if config.service == "Glacier":
      try:
          config.glacier.retrieve(glacier_archive_id)
      except Exception as e:
          click.echo(e)