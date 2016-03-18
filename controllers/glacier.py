from cement.core.controller import CementBaseController, expose
from extensions.glacier import GlacierClient

class GlacierController(CementBaseController):
    class Meta:
        label = 'base'
        description = "ValleyWorks Backup Manager"
        arguments = [
            (['extra_arguments'], dict(action='store', nargs='*'))
            ]



    def _setup(self, obj):
        # always run core setup first
        super(GlacierController, self)._setup(obj)

        self.ACCESS_KEY_ID = self.app.config.get('base', 'ACCESS_KEY_ID')
        self.SECRET_ACCESS_KEY = self.app.config.get('base', 'SECRET_ACCESS_KEY')
        self.VAULT_NAME = self.app.config.get('glacier', 'VAULT_NAME')
        self.AWS_ACCOUNT_ID = self.app.config.get('base', 'AWS_ACCOUNT_ID')

        self.glacier = GlacierClient(self.VAULT_NAME,
                                self.ACCESS_KEY_ID,
                                self.SECRET_ACCESS_KEY,
                                self.AWS_ACCOUNT_ID)
    @expose(help="Backup a file to glacier")
    def backup(self):
        """Store a file in a Glacier Vault

        Parameters
        ----------
        filename : str
        """
        if len(self.app.pargs.extra_arguments) == 0:  # has extra arguments
            self.app.log.error('Must have arguments')
            return
        filename = os.path.split(self.app.pargs.extra_arguments[0])[1] # Removes absolute path if there is one
        self.app.log.info("Uploading file %s" % filename)

        p = progress_bar_loading()
        # p.start()

        try:
            response = self.glacier.upload(filename)

            if response:
                self.app.log.info("File %s uploaded." % filename)
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
        """Requests a backup from Glacier

        Parameters
        ----------
            id : str
                The AWS Glacier archive id

        """
        if len(self.app.pargs.extra_arguments) == 0:  # has extra arguments
            self.app.log.error('Must have Archive ID')
            return

        archive_id = self.app.pargs.extra_arguments[0]
        self.app.log.info("Retrieving %s" % archive_id)
    
        glacier_archive_id = db.get_archive_id(archive_id)

        try:
            self.glacier.retrieve(glacier_archive_id)
        except Exception as e:
            self.app.log.error(e)

    @expose(help="download a finished archive retrieval")
    def download_file(self):
        """Gets a ready-to-be-downloaded file from Glacier

        Parameters
        ----------

        job_id : str
        """
        if len(self.app.pargs.extra_arguments) == 0:  # has extra arguments
            self.app.log.error('Must have Job ID')
            return

        job_id = self.app.pargs.extra_arguments[0]
        response = self.glacier.download_file(job_id)

    @expose(help="List archives on glacier")
    def list_files(self):
        """Outputs a list of backed up files
        """
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