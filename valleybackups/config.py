import ConfigParser
import os

Config = ConfigParser.SafeConfigParser()
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'valleybackups.conf')

def create_config_file(CONFIG_FILE):
    parser = ConfigParser.SafeConfigParser()

    parser.add_section('base')
    parser.set('base', 'ACCESS_KEY_ID', '')
    parser.set('base', 'SECRET_ACCESS_KEY', '')
    parser.set('base', 'AWS_ACCOUNT_ID', '')

    parser.add_section('glacier')
    parser.set('glacier', 'VAULT_NAME','')

    opened_file = open(CONFIG_FILE, 'w')
    parser.write(opened_file)
    opened_file.close()

if os.path.isfile(CONFIG_FILE):
    pass
else:
    create_config_file(CONFIG_FILE)


Config.read(CONFIG_FILE)


def get_config(section, option):
    return Config.get(section, option)







def check_config():
    config_ok = False
    for section_name in Config.sections():
        for name, value in Config.items(section_name):
            if value != '':
                config_ok = True
            else:
                config_ok = False
    return config_ok



def get_parser():
  return Config
