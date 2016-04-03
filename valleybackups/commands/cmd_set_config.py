import click
from valleybackups.config_context import pass_config


@click.command()
@click.argument('section', required=True, type=str)
@click.argument('setting', required=True, type=str)
@click.argument('value', required=True, type=str)
@pass_config
def cli(config, section, setting, value):
    """Sets value to a specific configuration item"""
    click.echo("Changing option %s.%s to %s" % (section, setting, value))

    if config.handler.set_config(section, setting, value):
        config.handler.save_config()
    else:
        raise click.ClickException("Please enter a valid setting name")
