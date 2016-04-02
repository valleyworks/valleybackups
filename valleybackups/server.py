from config_handler import ConfigurationHandler
from flask import Flask, request
from logging.handlers import RotatingFileHandler
from extensions.glacier import GlacierClient
from valleybackups import db
import requests
import json
import logging

app = Flask(__name__)

try:
    config_handler = ConfigurationHandler()

    glacier = GlacierClient(config_handler.get_config('glacier', 'VAULT_NAME'),
                            config_handler.get_config('base', 'ACCESS_KEY_ID'),
                            config_handler.get_config('base', 'SECRET_ACCESS_KEY'),
                            config_handler.get_config('base', 'AWS_ACCOUNT_ID'),
                            config_handler.get_config('base', 'REGION_NAME'))
except Exception as e:
    print "Invalid Configuration"
    exit()

def msg_process(msg, tstamp):
    js = json.loads(msg)

    job_id = js["JobId"]

    app.logger.info("Processing job: %s with status: %s" % (job_id, js["StatusCode"]))
    # Updates job status
    db.update_job(job_id, js["StatusCode"])

    if js["StatusCode"] == "Succeeded":
        app.logger.info("Downloading File... | Job: %s" % job_id)
        glacier.download_file(job_id)


@app.route('/', methods=['GET', 'POST', 'PUT'])
def sns():
    """AWS sends JSON with text/plain mimetype"""
    js = json.loads(request.data)

    hdr = request.headers.get('X-Amz-Sns-Message-Type')
    # subscribe to the SNS topic
    if hdr == 'SubscriptionConfirmation' and 'SubscribeURL' in js:

        # Subscribing to AWS SNS ... TODO: Refactor to use boto3
        subscription = requests.get(js['SubscribeURL'])

        if subscription:
            app.logger.info("Subscription Confirmed Correctly!")

    if hdr == 'Notification':
        msg_process(js['Message'], js['Timestamp'])

    return 'OK\n'


def run_server():
    # db.init_mapping()

    handler = RotatingFileHandler('snsListener.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)

    app.run(
        host="0.0.0.0",
        # port = 5000,
        debug=True
    )

if __name__ == '__main__':
    db.init_mapping()

    handler = RotatingFileHandler('snsListener.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)

    app.run(
        host="0.0.0.0",
        debug=True
    )
