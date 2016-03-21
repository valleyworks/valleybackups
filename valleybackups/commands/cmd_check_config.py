import click
from valleybackups.config import get_parser, check_config
from valleybackups.cli import pass_config

@click.command()
@pass_config
def cli(config):
  config_ok = check_config()
  click.echo('OK' if config_ok else 'Missing Values')