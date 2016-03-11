from flask import Flask, request
import logging
from logging.handlers import RotatingFileHandler
import requests
import json
import db
from valleybackups import get_config
from extensions.GlacierVault import GlacierVault

app = Flask(__name__)

glacier = GlacierVault(get_config('glacier','VAULT_NAME'),
                       get_config('base','ACCESS_KEY_ID'),
                       get_config('base','SECRET_ACCESS_KEY'),
                       get_config('base','AWS_ACCOUNT_ID'))

def msg_process(msg, tstamp):
    js = json.loads(msg)
    # msg = 'Region: {0} / Alarm: {1}'.format(
    #    js['Region'], js['AlarmName']
    # )

    archiveId = js["ArchiveId"]
    jobId = js["JobId"]

    # Updates job status
    db.update_job(jobId, js["StatusCode"])

    if js["StatusCode"] == "Succeeded":
        app.logger.info("Downloading File... | Job: %s" % jobId)
        glacier.download_file(jobId)

@app.route('/', methods = ['GET', 'POST', 'PUT'])
def sns():
    # AWS sends JSON with text/plain mimetype
    try:
        js = json.loads(request.data)
    except:
        pass


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

if __name__ == '__main__':
    db.init_mapping()

    handler = RotatingFileHandler('snsListener.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)


    app.logger.addHandler(handler)

    app.run(
        # host = "0.0.0.0",
        # port = 5000,
        debug = True
    )
