import os
import click
from click import ClickException
import sys

from valleybackups import db
from config import get_config, check_config
from extensions.glacier import GlacierClient

class Config(object):
    def __init__(self):
        self.debug = False
        self.ACCESS_KEY_ID = get_config('base', 'ACCESS_KEY_ID')
        self.SECRET_ACCESS_KEY = get_config('base', 'SECRET_ACCESS_KEY')
        self.VAULT_NAME = get_config('glacier', 'VAULT_NAME')
        self.AWS_ACCOUNT_ID = get_config('base', 'AWS_ACCOUNT_ID')
        self.glacier = GlacierClient(self.VAULT_NAME,
                                self.ACCESS_KEY_ID,
                                self.SECRET_ACCESS_KEY,
                                self.AWS_ACCOUNT_ID)
        self.glacier.init_vault(self.AWS_ACCOUNT_ID, self.VAULT_NAME)

pass_config = click.make_pass_decorator(Config, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'commands'))


class ComplexCLI(click.MultiCommand):

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

        except ImportError as e:
            return

        return mod.cli


@click.command(cls=ComplexCLI)
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
        if check_config():
            db.init(get_config('glacier', 'VAULT_NAME'), debug)
        else:
            if get_config('glacier', 'VAULT_NAME') == '':
                raise click.ClickException("You need to specify a vault, or create one with create_vault [vault_name]")
            raise click.ClickException("Invalid Configuration")
