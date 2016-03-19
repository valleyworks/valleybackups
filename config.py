import ConfigParser
import os

Config = ConfigParser.ConfigParser()
Config.read(os.path.join(os.path.dirname(__file__), 'valleybackups.conf'))

def get_config(section, option):
  return Config.get(section, option)