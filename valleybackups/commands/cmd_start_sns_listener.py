import click
from valleybackups.config_context import pass_config
from valleybackups.server import run_server


@click.command()
@click.argument('port', type=int, default=5000)
@pass_config
def cli(config, port):
    """Starts a http server to get Amazon SNS Notifications"""
    run_server()
