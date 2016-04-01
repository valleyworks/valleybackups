from os.path import abspath, join, dirname
from os import listdir
import click
from sys import version_info
from valleybackups.config_context import pass_config
from valleybackups.db import init


cmd_folder = abspath(join(dirname(__file__), 'commands'))


class ValleybackupsCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in listdir(cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('valleybackups.commands.cmd_' + name,
                             None, None, ['cli'])

        except ImportError as e:
            return

        return mod.cli


@click.command(cls=ValleybackupsCLI)
@click.option('-d', '--debug', is_flag=True, help='Enables debug mode.')
@click.option('-s', '--service', default='Glacier')
@pass_config
@click.pass_context
def cli(context, config, debug, service):
    """A complex command line interface."""
    config.debug = debug
    config.service = service

    if not context.invoked_subcommand.endswith('config') and not context.invoked_subcommand == 'create_vault':
        try:
            if config.handler.check_config():
                init(config.VAULT_NAME, debug)
            else:
                if config.VAULT_NAME == '':
                    raise click.ClickException("You need to specify a vault, or create one with create_vault [vault_name]")
                raise click.ClickException("Invalid Configuration")
        except Exception as e:
            raise click.ClickException(e.message)
