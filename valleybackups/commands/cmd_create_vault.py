import click

from valleybackups.cli import pass_config
from valleybackups.config import get_parser, CONFIG_FILE


@click.command()
@click.argument('vault_name', type=str)
@pass_config
def cli(config, vault_name):
    """Gets a ready-to-be-downloaded file from Glacier. """
    if config.service == "Glacier":
        response = config.glacier.create_vault(vault_name)
        if response:
            click.echo("Vault %s successfully created" % vault_name)
            parser = get_parser()
            parser.set('glacier', 'VAULT_NAME', vault_name)

            opened_file = open(CONFIG_FILE, 'w')
            parser.write(opened_file)
            opened_file.close()
