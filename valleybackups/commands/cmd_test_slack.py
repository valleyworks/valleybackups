import click
import requests
from valleybackups.config_context import pass_config
import pdb
import json
@click.command()
@pass_config
def cli(config):
    payload = {"text": "Just to let you know.\nI've uploaded your 20160801-dump.sql.gz to AWS Glacier."}
    r = requests.post(config.WEBHOOK_URL, data = json.dumps(payload))
    if (r.status_code != 200):
        print (r.text)
