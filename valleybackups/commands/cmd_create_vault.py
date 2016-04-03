import click

from valleybackups.config_context import pass_config
from valleybackups import db


@click.command()
@click.argument('vault_name', type=str)
@pass_config
def cli(config, vault_name):
    """Creates a new Vault in Glacier"""
    if config.service == "Glacier":
        response = config.glacier.create_vault(vault_name)
        if response:
            click.echo("Vault %s successfully created" % vault_name)
            if config.handler.set_config('glacier', 'VAULT_NAME', vault_name):
                config.handler.save_config()
                db.init_mapping()
                db.create_vault(vault_name, "Glacier")
