import click
from valleybackups import db


@click.command()
@click.option('-c', '--count', is_flag=True)
def cli(count):
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
