import click
from valleybackups import db
from math import ceil

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
      print "ID - NAME - SIZE - CREATED"
      for archive in archives:
        if archive.size:
            size = int(archive.size) / 1024.0 / 1024.0
            if format(size, '.2f') != '0.00':
                size = format(size, '.2f') + " mb"
            else:
                # Under 1 kb
                size = format(size * 1024 * 1024, '.0f') + " bytes"


        else:
            size = "Unknown"
        print " %s - %s - %s - %s" % (archive.id, archive.name, size, archive.created_at)
