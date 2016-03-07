from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from extensions.GlacierVault import GlacierVault
import db


class MyBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = "ValleyWorks Backup Manager"
        arguments = [
            (['extra_arguments'], dict(action='store', nargs='*'))
            ]

    @expose(hide=True)
    def default(self):
        self.app.args.parse_args(['--help'])

    @expose(help="Backup a file to glacier")
    def backup(self):
        if len(self.app.pargs.extra_arguments) == 0:  # has extra arguments
            self.app.log.error('Must have arguments')
            return

        ACCESS_KEY_ID = self.app.config.get('base', 'ACCESS_KEY_ID')
        SECRET_ACCESS_KEY = self.app.config.get('base', 'SECRET_ACCESS_KEY')
        VAULT_NAME = self.app.config.get('glacier', 'VAULT_NAME')

        self.app.log.info("Uploading file %s" %
                          self.app.pargs.extra_arguments[0])

        response = GlacierVault(VAULT_NAME,
                                ACCESS_KEY_ID,
                                SECRET_ACCESS_KEY).upload(
            self.app.pargs.extra_arguments[0]
        )

        if response:
            self.app.log.info("File %s uploaded." %
                              self.app.pargs.extra_arguments[0])
            db.create_archive(self.app.pargs.extra_arguments[0], VAULT_NAME, response)
        else:
            self.app.log.error("Error uploading file")

    @expose(aliases=['retrieve'], help="retrieves a archive")
    def download(self):
        if len(self.app.pargs.extra_arguments) == 0:  # has extra arguments
            self.app.log.error('Must have arguments')
            return

        ACCESS_KEY_ID = self.app.config.get('base', 'ACCESS_KEY_ID')
        SECRET_ACCESS_KEY = self.app.config.get('base', 'SECRET_ACCESS_KEY')
        VAULT_NAME = self.app.config.get('glacier', 'VAULT_NAME')

        self.app.log.info("Retrieving %s" % self.app.pargs.extra_arguments[0])
        try:
            GlacierVault(VAULT_NAME,
                         ACCESS_KEY_ID,
                         SECRET_ACCESS_KEY).retrieve(
                self.app.pargs.extra_arguments[0], True
            )
        except Exception as e:
            self.app.log.error(e)


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


with ValleyBackups() as app:
    # Parse a configuration file
    app.config.parse_file('./valleybackups.conf')

    db.init(app.config.get('glacier', 'VAULT_NAME'))

    app.run()
