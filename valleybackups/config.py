import ConfigParser
import os

def create_config_file(CONFIG_FILE):
  parser = ConfigParser.SafeConfigParser()

  parser.add_section('base')
  parser.set('base', 'ACCESS_KEY_ID', '')
  parser.set('base', 'SECRET_ACCESS_KEY', '')
  parser.set('base', 'AWS_ACCOUNT_ID', '')

  parser.add_section('glacier')
  parser.set('glacier', 'VAULT_NAME','')

  file = open(CONFIG_FILE, 'w')
  parser.write(file)
  file.close()

Config = ConfigParser.SafeConfigParser()
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'valleybackups.conf')

if os.path.isfile(CONFIG_FILE):
  pass
else:
  create_config_file(CONFIG_FILE)


Config.read(CONFIG_FILE)



def get_config(section, option):
  return Config.get(section, option)

def get_parser():
  return Config