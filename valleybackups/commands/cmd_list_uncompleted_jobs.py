import click

from valleybackups import db

@click.command()
def cli():
    """Outputs uncompleted jobs to the console
    """
    jobs = db.get_uncompleted_jobs()
    print "ID - ARCHIVE"
    for job in jobs:
        print " %s - %s" % (job[0], job[1])