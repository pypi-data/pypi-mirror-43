from invoke import task
from .lib import database as db_helper
from .lib.shell import shprint
from .lib.tasks import Tasks


@task
def drop(ctx, database):
    """
    Drop an odoo database.
    """
    Tasks.setup(ctx)
    db_helper.destroy_db(ctx, database)


@task(aliases=('list', ))
def ls(ctx):
    """
    List available postgres databases.
    """
    db_helper.query(ctx, db='postgres', sql='SELECT datname FROM pg_database WHERE datistemplate = false;')


@task
def make(ctx, name, modules='', verbose=False):
    """
    Create a new odoo database.
    """
    if modules == 'custom':
        modules = Tasks.details(ctx, 'all', names=True, custom_only=True, pretty=False, prints=False)
        modules = ','.join(modules)

    db = db_helper.configure_db(ctx, name, modules, verbose=verbose)
    shprint(ctx, msg='Created db {}.'.format(db))
