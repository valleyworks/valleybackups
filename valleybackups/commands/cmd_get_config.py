import click
from valleybackups.config_context import pass_config


@click.command()
@pass_config
def cli(config):
    parser = config.handler.get_parser()
    for section in parser.sections():
        print "[%s]" % section
        for name, value in parser.items(section):
            print '  %s = %r' % (name, value)
