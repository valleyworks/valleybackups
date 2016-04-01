import ConfigParser
from os.path import join, dirname, isfile


class ConfigurationHandler:
    def __init__(self):
        self.config_parser = ConfigParser.SafeConfigParser()
        self.config_file = join(dirname(__file__), 'valleybackups.conf')

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

        self.save_config()

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
