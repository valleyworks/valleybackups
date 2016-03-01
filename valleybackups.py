from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
import boto

class MyBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = "ValleyWorks Backup Manager"
        arguments = [
            (['-f', '--foo'],
             dict(action='store', help='the notorious foo option')),
            (['-C'],
             dict(action='store_true', help='the big C option')),
            (['extra_arguments'], dict(action='store', nargs='*'))
            ]

    @expose(hide=True)
    def default(self):
        self.app.log.info('Inside MyBaseController.default()')
        if self.app.pargs.foo:
            print("Recieved option: foo => %s" % self.app.pargs.foo)

    @expose(help="backup a file to glacier")
    def backup(self):
        if len(self.app.pargs.extra_arguments) == 0:  # has extra arguments
            self.app.log.error('Must have arguments')
            return

        ACCESS_KEY_ID = self.app.config.get('base', 'ACCESS_KEY_ID')
        SECRET_ACCESS_KEY = self.app.config.get('base', 'SECRET_ACCESS_KEY')
        VAULT_NAME = self.app.config.get('glacier', 'VAULT_NAME')

        # boto.connect_glacier is a shortcut return a Layer2 instance
        glacier_connection = boto.connect_glacier(
                                region_name="us-west-2",
                                aws_access_key_id=ACCESS_KEY_ID,
                                aws_secret_access_key=SECRET_ACCESS_KEY)

        self.app.log.info("Creating Glacier Vault %s" % VAULT_NAME)

        vault = glacier_connection.create_vault(VAULT_NAME)

        self.app.log.info("Backing up file...")

    @expose(aliases=['cmd2'], help="more of nothing")
    def command2(self):
        self.app.log.info("Inside MyBaseController.command2()")


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

    app.run()
