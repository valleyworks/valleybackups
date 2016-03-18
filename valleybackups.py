#!/usr/bin/python

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from extensions.GlacierVault import GlacierVault
from cement.core.exc import CaughtSignal
from extensions.progressbar import progress_bar_loading
import db
from os.path import dirname, abspath

class MyBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = "ValleyWorks Backup Manager"
        arguments = [
            (['extra_arguments'], dict(action='store', nargs='*'))
            ]



    def _setup(self, obj):
        # always run core setup first
        super(MyBaseController, self)._setup(obj)

        self.ACCESS_KEY_ID = self.app.config.get('base', 'ACCESS_KEY_ID')
        self.SECRET_ACCESS_KEY = self.app.config.get('base', 'SECRET_ACCESS_KEY')
        self.VAULT_NAME = self.app.config.get('glacier', 'VAULT_NAME')
        self.AWS_ACCOUNT_ID = self.app.config.get('base', 'AWS_ACCOUNT_ID')

        self.glacier = GlacierVault(self.VAULT_NAME,
                                self.ACCESS_KEY_ID,
                                self.SECRET_ACCESS_KEY,
                                self.AWS_ACCOUNT_ID)

    @expose(hide=True)
    def default(self):
        self.app.args.parse_args(['--help'])

    @expose(help="Backup a file to glacier")
    def backup(self):
        if len(self.app.pargs.extra_arguments) == 0:  # has extra arguments
            self.app.log.error('Must have arguments')
            return

        self.app.log.info("Uploading file %s" %
                          self.app.pargs.extra_arguments[0])

        p = progress_bar_loading()
        # p.start()

        try:
            response = self.glacier.upload(
                self.app.pargs.extra_arguments[0]
            )

            if response:
                self.app.log.info("File %s uploaded." %
                                  self.app.pargs.extra_arguments[0])
                # db.create_archive(self.app.pargs.extra_arguments[0], response.vault_name, response.id)
            else:
                self.app.log.error("Error uploading file")
            p.stop()

        except CaughtSignal as e:
            p.kill()
        except KeyboardInterrupt or EOFError:
            p.kill()

    @expose(help="initiates archive retrieval")
    def request_file(self):
        if len(self.app.pargs.extra_arguments) == 0:  # has extra arguments
            self.app.log.error('Must have arguments')
            return

        self.app.log.info("Retrieving %s" % self.app.pargs.extra_arguments[0])
	
	archive_id = db.get_archive_id(self.app.pargs.extra_arguments[0])

        try:
            self.glacier.retrieve(archive_id, True)
        except Exception as e:
            self.app.log.error(e)

    @expose(help="download a finished archive retrieval")
    def download_file(self):
        """
        .. py:function:: enumerate(sequence[, start=0])
        """
        if len(self.app.pargs.extra_arguments) == 0:  # has extra arguments
            self.app.log.error('Must have arguments')
            return

        response = self.glacier.download_file(
            self.app.pargs.extra_arguments[0]
        )

    @expose(help="List archives on glacier")
    def list_files(self):
	archives = db.get_files()
	print "ID - NAME"
	for archive in archives:
	    print " %s - %s" % (archive.id, archive.name)

    @expose(help="List uncompleted jobs")
    def list_uncompleted_jobs(self):
	"""Outputs uncompleted jobs to the console
        """
	jobs = db.get_uncompleted_jobs()
	print "ID - ARCHIVE"
	for job in jobs:
	     print " %s - %s" % (job[0], job[1])

class MySecondController(CementBaseController):
    class Meta:
        label = 'second'
        stacked_on = 'base'

    @expose(help='this is some command', aliases=['some-cmd'])
    def second_cmd1(self):
        self.app.log.info("Inside MySecondController.second_cmd1")


class ValleyBackups(CementApp):

    class Meta:
        label = 'valleybackups'
        base_controller = 'base'
        handlers = [MyBaseController, MySecondController]
        config_files = [abspath(dirname(__file__)) + '/valleybackups.conf']


with ValleyBackups() as app:
    def get_config(section, key):
        return app.config.get(section, key)

    # If running python valleybackups.py
    if __name__ == '__main__':
        db.init(app.config.get('glacier', 'VAULT_NAME'), app.debug)
        app.run()
