import click
from valleybackups.config_context import pass_config


@click.command()
@pass_config
def cli(config):
    config_ok = config.handler.check_config()
    click.echo('OK' if config_ok else 'Missing Values')
