import click
from valleybackups import db
from valleybackups.config_context import pass_config


@click.command()
@click.argument('archive_id', type=int)
@pass_config
def cli(config, archive_id):
    """Requests a backup from Glacier
    """

    # TODO: don't request a already requested file

    exist = db.check_dup_requested_file(archive_id)

    if not exist:
        click.echo("Retrieving %s" % archive_id)

        glacier_archive_id = db.get_archive_id(archive_id)

        if config.service == "Glacier":
            try:
                config.glacier.retrieve(glacier_archive_id)
            except Exception as e:
                click.echo(e)
    else:
        raise click.ClickException(message="This file has been already requested")
