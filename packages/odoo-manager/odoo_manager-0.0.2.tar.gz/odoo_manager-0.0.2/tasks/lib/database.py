import time
from . import configs
from . import paths as path_helpers
from . helpers import shprint, redirect
from . tasks import Tasks

pipe_dev_null = path_helpers.pipe_dev_null


def configure_db(ctx, db, modules, verbose=False, container='web'):
    """
    :param ctx {invoke.context.Context}: Invoke context variable
    :param db {str}: The name of the database
    :param modules {str}: Comma separated list of modules
    :return {str}: The name of the created database
    """

    # We have to take down the current running containers before running
    # the command to generate databases, build the mounts will conflict
    # for some reason. We will bring it back up before returning.
    Tasks.down(ctx)

    # If there's no db arg passed in then we assume that the user wants
    # us to automatically create the db for them. In this case we are just
    # going to spin up a unique name based on the current timestamp in seconds.
    shprint(ctx, msg='Configuring a new database...')
    if not db:
        db = "tester_" + str(int(time.time()))

    if verbose:
        shprint(ctx, msg='    *Setting db name {}...'.format(db))
    odoo_exe = configs.config.get('options', 'ODOO_EXE')
    odoo_version = configs.config.get('options', 'ODOO_VERSION')
    cmd = "docker-compose run {ct} {exe} -c {conf}{dt} --xmlrpc-port={web_port} --longpolling-port={poll_port} --stop-after-init -d {db} -i {mods} {extras}"
    cmd = cmd.format(ct=container,
                     exe='/opt/odoo/core/{}'.format(odoo_exe),
                     conf='/opt/odoo/config/odoo.conf',
                     dt='' if odoo_version in ['9.0', '10.0'] else ' -p $(date +%s)',
                     web_port='7777',
                     poll_port='7788',
                     db=db,
                     mods=modules,
                     extras='--logfile=None --log-level=info --log-handler=:INFO' if verbose else '')

    if verbose:
        shprint(ctx, msg='    *Running init db...')
        shprint(ctx, msg='    *{}'.format(cmd))
    ctx.run(cmd)

    Tasks.run(ctx, detach=True, verbose=verbose)
    return db


def destroy_db(ctx, db, verbose=False, container='db'):
    """
    Drop a database.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param db {str}: The name of the database to drop
    :return {NoneType}:
    """
    if verbose:
        shprint(ctx, msg='Cleaning up database {}...'.format(db))
    try:
        destroy_db_sessions(ctx, db, verbose=verbose, container=container)
        Tasks.ssh(ctx, container, executable='dropdb -U odoo {db}'.format(db=db))
        shprint(ctx, msg='Database {} dropped.'.format(db))
    except Exception as e:
        shprint(ctx, msg='There was problem dropping the database.', color='red')
        if verbose:
            shprint(ctx, msg=str(e), color='red')


def destroy_db_sessions(ctx, db, verbose=False, container='db'):
    sql = """SELECT pg_terminate_backend(pg_stat_activity.pid)
               FROM pg_stat_activity
               WHERE pg_stat_activity.datname = '{}'
                   AND pid <> pg_backend_pid();""".format(db)
    query(ctx, db, sql, quiet=not verbose, container=container)


def query(ctx, db, sql, quiet=False, container='db'):
    exe = 'psql -U odoo {db} -c "{query}"{extras}'.format(db=db, query=sql, extras=' -q' if quiet else '')
    Tasks.ssh(ctx, container, executable=exe, quiet=quiet)
