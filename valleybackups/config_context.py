from valleybackups.extensions.glacier import GlacierClient
import click
from valleybackups.config_handler import ConfigurationHandler


class ConfigContext(object):
    def __init__(self):
        self.debug = False
        self.handler = ConfigurationHandler()
        self.VAULT_NAME = self.handler.get_config('glacier', 'VAULT_NAME')
        self.ACCESS_KEY_ID = self.handler.get_config('base', 'ACCESS_KEY_ID')
        self.SECRET_ACCESS_KEY = self.handler.get_config('base', 'SECRET_ACCESS_KEY')
        self.AWS_ACCOUNT_ID = self.handler.get_config('base', 'AWS_ACCOUNT_ID')
        self.REGION_NAME = self.handler.get_config('base', 'REGION_NAME')

        self.glacier = GlacierClient(self.VAULT_NAME,
                                     self.ACCESS_KEY_ID,
                                     self.SECRET_ACCESS_KEY,
                                     self.AWS_ACCOUNT_ID,
                                     self.REGION_NAME)

        self.glacier.init_vault(self.AWS_ACCOUNT_ID, self.VAULT_NAME)

pass_config = click.make_pass_decorator(ConfigContext, ensure=True)
