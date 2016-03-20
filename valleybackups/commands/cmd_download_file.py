import click

from valleybackups.cli import pass_config
@click.command()
@click.argument('job_id', type=str)
@pass_config
def cli(config, job_id):
    """Gets a ready-to-be-downloaded file from Glacier. """
    if config.service == "Glacier":
      response = config.glacier.download_file(job_id)