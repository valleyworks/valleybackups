import click

from valleybackups.config_context import pass_config
from valleybackups.db import job_exists, get_job, check_dup_requested_file, get_archive_id, get_job_for_archive, delete_job
from valleybackups.exceptions import JobNotFound


@click.command()
@click.argument('archive_id', type=str)
@pass_config
def cli(config, archive_id):
    """Gets a ready-to-be-downloaded file from Glacier. """

    if config.service == "Glacier":
        try:
            glacier_archive_id = get_archive_id(archive_id)

            if check_dup_requested_file(archive_id):
                # Try to download previously created JOB
                job = get_job_for_archive(archive_id)

                click.echo("Re-trying download...")
                config.glacier.download_file(job.job_id)
            else:
                job_id = config.glacier.retrieve(glacier_archive_id)
                click.echo("File has been requested for download.")

            """
            if not job:
                raise click.ClickException(message="The requested file does not exist in our database, "
                                                   "please check with list_uncompleted_jobs command")
            if not job_exists(job.job_id):
                raise click.ClickException(message="This file has not been uploaded from this machine")
            """
        except JobNotFound:
            delete_job(job.id)
            job_id = config.glacier.retrieve(glacier_archive_id)
            click.echo("File has been requested for download.")
        except Exception as e:
            raise click.ClickException(e.message)
