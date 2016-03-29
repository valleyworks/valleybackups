from extensions.glacier import GlacierClient
import click
import ConfigParser
import os




class ConfigContext(object):
    def __init__(self):
        self.debug = False
        self.handler = ConfigurationHandler()
        self.VAULT_NAME = self.handler.get_config('glacier', 'VAULT_NAME')
        self.ACCESS_KEY_ID = self.handler.get_config('base', 'ACCESS_KEY_ID')
        self.SECRET_ACCESS_KEY = self.handler.get_config('base', 'SECRET_ACCESS_KEY')
        self.AWS_ACCOUNT_ID = self.handler.get_config('base', 'AWS_ACCOUNT_ID')

        self.glacier = GlacierClient(self.VAULT_NAME,
                                     self.ACCESS_KEY_ID,
                                     self.SECRET_ACCESS_KEY,
                                     self.AWS_ACCOUNT_ID)

        self.glacier.init_vault(self.AWS_ACCOUNT_ID, self.VAULT_NAME)

pass_config = click.make_pass_decorator(ConfigContext, ensure=True)


class ConfigurationHandler():
    def __init__(self):
        self.config_parser = ConfigParser.SafeConfigParser()
        self.config_file = os.path.join(os.path.dirname(__file__), 'valleybackups.conf')

        if os.path.isfile(self.config_file):
            pass
        else:
            self.create_config_file(self.config_file)

        self.config_parser.read(self.config_file)


    def create_config_file(self):
        self.config_parser.add_section('base')
        self.config_parser.set('base', 'ACCESS_KEY_ID', '')
        self.config_parser.set('base', 'SECRET_ACCESS_KEY', '')
        self.config_parser.set('base', 'AWS_ACCOUNT_ID', '')

        self.config_parser.add_section('glacier')
        self.config_parser.set('glacier', 'VAULT_NAME', '')

        opened_file = open(self.config_file, 'w')
        self.config_parser.write(opened_file)
        opened_file.close()

    def get_config(self, section, option):
        return self.config_parser.get(section, option)

    def set_config(self, section, option, value):
        self.config_parser.set(section, option, value)

    def check_config(self):
        config_ok = False
        for section_name in self.config_parser.sections():
            for name, value in self.config_parser.items(section_name):
                if value != '':
                    config_ok = True
                else:
                    config_ok = False
        return config_ok

    def get_parser(self):
        return self.config_parser

    def save_config(self):
        opened_file = open(self.config_file, 'w')
        self.config_parser.write(opened_file)
        opened_file.close()
