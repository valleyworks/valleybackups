#!/usr/bin/python

from cement.core.foundation import CementApp
from cement.core.exc import CaughtSignal
from extensions.progressbar import progress_bar_loading
from os.path import dirname, abspath
import os
from controllers.glacier import GlacierController
import db


class ValleyBackups(CementApp):
    """Base class, this is being done this way so in the future, the behaviour
    can be extended with new handlers (FTP, S3, who knows!)
    """
    class Meta:
        label = 'valleybackups'
        base_controller = 'base'
        handlers = [GlacierController]
        config_files = [abspath(dirname(__file__)) + '/valleybackups.conf']


with ValleyBackups() as app:
    def _get_config(section, key):
        return app.config.get(section, key)

    # If running python valleybackups.py
    if __name__ == '__main__':
        db.init(app.config.get('glacier', 'VAULT_NAME'), app.debug)
        app.run()
