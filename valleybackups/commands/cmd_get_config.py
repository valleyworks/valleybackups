import click
from valleybackups.config import get_parser
from valleybackups.cli import pass_config

@click.command()
@pass_config
def cli(config):
  parser = get_parser()
  for section in parser.sections():
    print "[%s]" % section
    for name, value in parser.items(section):
        print '  %s = %r' % (name, value)