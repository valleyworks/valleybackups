import click
from valleybackups.config import get_parser, CONFIG_FILE
from valleybackups.cli import pass_config

@click.command()
@click.argument('section', required=True, type=str)
@click.argument('setting', required=True, type=str)
@click.argument('value', required=True, type=str)
@pass_config
def cli(config, section, setting, value):
  click.echo("Changing option %s.%s to %s" % (section, setting, value))

  parser = get_parser()
  parser.set(section, setting, value)
  

  file = open(CONFIG_FILE, 'w')
  parser.write(file)
  file.close()
