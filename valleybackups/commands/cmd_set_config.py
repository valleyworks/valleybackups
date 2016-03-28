import click
from valleybackups.config import get_parser, CONFIG_FILE


@click.command()
@click.argument('section', required=True, type=str)
@click.argument('setting', required=True, type=str)
@click.argument('value', required=True, type=str)
def cli(section, setting, value):
    """Sets value to a specific configuration item"""
    click.echo("Changing option %s.%s to %s" % (section, setting, value))

    parser = get_parser()
    parser.set(section, setting, value)

    opened_file = open(CONFIG_FILE, 'w')
    parser.write(opened_file)
    opened_file.close()
