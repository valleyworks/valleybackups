import click

from valleybackups.config_context import pass_config
from valleybackups.db import job_exists, get_job


@click.command()
@click.argument('job_id', type=str)
@pass_config
def cli(config, job_id):
    """Gets a ready-to-be-downloaded file from Glacier. """
    if config.service == "Glacier":
        job = get_job(job_id)
        if not job_exists(job.job_id):
            raise click.ClickException(message="This file has not been uploaded from this machine")
    try:
        response = config.glacier.download_file(job.job_id)
    except Exception as e:
        raise click.ClickException(e.message)
