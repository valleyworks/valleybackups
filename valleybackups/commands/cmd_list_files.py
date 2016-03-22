import click
from valleybackups import db
from valleybackups.cli import pass_config

@click.command()
@click.option('-c', '--count', is_flag=True)
@pass_config
def cli(config, count):
    """Outputs a list of backed up files
    """

    if count:
      files = db.count_files()
      click.echo("Number of files on inventory: %s" % files)
    else:
      archives = db.get_files()
      print "ID - NAME - CREATED"
      for archive in archives:
        print " %s - %s - %s" % (archive.id, archive.name, archive.created_at)