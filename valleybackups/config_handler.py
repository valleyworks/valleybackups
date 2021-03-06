import ConfigParser
from os import chmod, makedirs
from os.path import join, dirname, isfile, exists
import stat
from valleybackups.util import get_platform
platform = get_platform()


class ConfigurationHandler:
    def __init__(self, config_name="valleybackups.conf"):
        self.valid_config = [
            "ACCESS_KEY_ID",
            "SECRET_ACCESS_KEY",
            "AWS_ACCOUNT_ID",
            "REGION_NAME",
            "VAULT_NAME"
        ]
        self.config_parser = ConfigParser.SafeConfigParser()

        if platform in ("linux","osx"):
          directory = "/usr/local/etc/valleybackups"
          if not exists(directory):
            makedirs(directory)
            chmod(directory, int('777', 8))

          self.config_file = join(directory, config_name)
        else:
          self.config_file = join(dirname(__file__), config_name)

        if isfile(self.config_file):
            pass
        else:
            self.create_config_file()

        self.config_parser.read(self.config_file)

    def create_config_file(self):
        self.config_parser.add_section('base')
        self.config_parser.set('base', 'ACCESS_KEY_ID', '')
        self.config_parser.set('base', 'SECRET_ACCESS_KEY', '')
        self.config_parser.set('base', 'AWS_ACCOUNT_ID', '')
        self.config_parser.set('base', 'REGION_NAME', '')

        self.config_parser.add_section('glacier')
        self.config_parser.set('glacier', 'VAULT_NAME', '')

        self.save_config(change_permissions=True)

    def get_config(self, section, option):
        return self.config_parser.get(section, option)

    def set_config(self, section, option, value):
        if option.upper() not in self.valid_config:
            return False
        self.config_parser.set(section, option, value)
        return True

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

    def save_config(self, change_permissions=False):
        opened_file = open(self.config_file, 'w')
        self.config_parser.write(opened_file)
        opened_file.close()
        if change_permissions:
          chmod(self.config_file, int('777', 8))
