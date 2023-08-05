import os
from invoke import task
from .lib import paths as path_helpers
from .lib.shell import shprint
from .lib.tasks import Tasks
from .lib.helpers import snippet

paths = path_helpers.Paths()
YES_OPTIONS = ('y', 'ye', 'yes', 'ya')


@task
def model(ctx, name, path, inherit=None, views=('form', 'tree', 'kanban')):
    """
    Coming soon.

    :param ctx {invoke.context.Context}: Invoke context variable
    """
    Tasks.setup(ctx)
    shprint(ctx, msg='Coming soon...')


@task
def test(ctx, class_name, path, verbose=False, yes=False):
    """
    Coming soon.

    :param ctx {invoke.context.Context}: Invoke context variable
    """
    Tasks.setup(ctx)
    if os.path.isfile(paths.base(path)):
        if not yes and input('There is already a file at {}. Do you want to override it (y/n)? '.format(path)) not in YES_OPTIONS:
            return
        ctx.run('touch {}'.format(paths.base(path)))

    shprint(ctx, msg='Generating test snippet...')
    contents = snippet(paths.base('tasks/snippets/test.snippet'), data={'class_name': class_name}, out=paths.base(path))
    if verbose:
        shprint(ctx, msg=contents, color='lightblue')
    shprint(ctx, msg='Done.')


@task
def view(ctx, name, type, model=None):
    """
    Coming soon.

    :param ctx {invoke.context.Context}: Invoke context variable
    """
    Tasks.setup(ctx)
    shprint(ctx, msg='Coming soon...')


@task
def action(ctx, name, type, model=None):
    """
    Coming soon.

    :param ctx {invoke.context.Context}: Invoke context variable
    """
    Tasks.setup(ctx)
    shprint(ctx, msg='Coming soon...')


@task
def rule(ctx):
    """
    Coming soon.

    :param ctx {invoke.context.Context}: Invoke context variable
    """
    Tasks.setup(ctx)
    shprint(ctx, msg='Coming soon...')


@task
def access(ctx):
    """
    Coming soon.

    :param ctx {invoke.context.Context}: Invoke context variable
    """
    Tasks.setup(ctx)
    shprint(ctx, msg='Coming soon...')


@task
def stylesheet(ctx):
    """
    Coming soon.

    :param ctx {invoke.context.Context}: Invoke context variable
    """
    Tasks.setup(ctx)
    shprint(ctx, msg='Coming soon...')


@task
def script(ctx):
    """
    Coming soon.

    :param ctx {invoke.context.Context}: Invoke context variable
    """
    Tasks.setup(ctx)
    shprint(ctx, msg='Coming soon...')
