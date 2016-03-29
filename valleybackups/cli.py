import os
import click
import sys

from valleybackups import db
# from config import check_config
from configuration_handler import pass_config

cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'commands'))


class ValleybackupsCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('valleybackups.commands.cmd_' + name,
                             None, None, ['cli'])

        except ImportError:
            return

        return mod.cli


@click.command(cls=ValleybackupsCLI)
@click.option('-d', '--debug', is_flag=True,
              help='Enables debug mode.')
@click.option('-s', '--service', default='Glacier')
@pass_config
@click.pass_context
def cli(context, config, debug, service):
    """A complex command line interface."""
    config.debug = debug
    config.service = service

    if not context.invoked_subcommand.endswith('config') and not context.invoked_subcommand == 'create_vault':
        if config.handler.check_config():
            db.init(config.VAULT_NAME, debug)
        else:
            if config.VAULT_NAME == '':
                raise click.ClickException("You need to specify a vault, or create one with create_vault [vault_name]")
            raise click.ClickException("Invalid Configuration")
