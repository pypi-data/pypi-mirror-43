from invoke import task
from .lib import validation
from .lib.tasks import Tasks


@task(default=True)
def run(ctx, rebuild=False, update=False, args='', detach=False, compose='', verbose=False):
    """
    Run an Odoo instance based on this collection/project.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param rebuild:
    :param update:
    :param args:
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    if validation.can_run(ctx):
        Tasks.run(ctx, rebuild, update, args, detach, compose, verbose)


@task
def shell(ctx, db):
    """
    The same as run except running the application with the Odoo shell command
    so that you can access the Odoo shell command line interface.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param db:
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.run_shell(ctx, db)
