import os
import time
from invoke import task
from .lib import paths as path_helpers
from .lib.tasks import Tasks
from .lib.shell import shprint

paths = path_helpers.Paths()


@task(default=True)
def test(ctx, modules, db='', verbose=False, coverage=False, yes=False, sudo=False, ci=False):
    """
    Run all of the tests associated with this collection/project.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param modules {str}:
    :param db {str}:
    :param verbose {bool}:
    :param coverage {bool}:
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.test(ctx, modules, db, verbose, coverage, yes, sudo, ci)


@task
def profile(ctx, seconds=30, idle=True, color=None, dev_tools=False):
    """
    Runs a profile of the running odoo instance.

    This will attach itself to the main process on the web container.

    Some requirements before running:

    1. Make sure you have a profiler folder that is mapped inside the container
       at /opt/odoo/profiler.
    2. Make sure that pyflame and flamegraph exist inside the container and is
       owned by the odoo user.
    3. Make sure that your odoo instance is using /var/run/odoo.pid

    TODO:
        - Add flag for removing core functions
        - Also print a stack trace in the command line showing perf if possible
          through pyflame

    :param ctx {invoke.context.Context}: Invoke context variable
    :param db {str}:
    """
    shprint(ctx, msg='Getting profiler setup...')
    Tasks.setup(ctx)

    if not color:
        color = 'green'

    filename = '{time}'.format(time=int(round(time.time() * 1000))) + ('.cpuprofile' if dev_tools else '.svg')
    out_file = '/opt/odoo/profiler/{}'.format(filename)
    cmd = 'bash -c \'cat {pid} | xargs -t -I PORT bash -c \"{pyflame_exe} -s {seconds} {chart} -p PORT\" | {reporter} > {out}\''
    to_flamegraph = '/opt/flamegraph/flamegraph.pl --width 1600 --inverted --colors {colors}'.format(colors=color)
    to_dev_tools = '/opt/pyflame/utils/flame-chart-json'

    exe = cmd.format(pid='/var/run/odoo.pid',
                     pyflame_exe='/opt/pyflame/src/pyflame',
                     seconds=seconds,
                     chart='--flamechart' if dev_tools else '',
                     reporter=to_dev_tools if dev_tools else to_flamegraph,
                     out=out_file)

    try:
        shprint(ctx, msg='Profile will run for {seconds} seconds.'.format(seconds=seconds))
        shprint(ctx, msg='Profiler started...')
        Tasks.ssh(ctx, container='web', executable=exe, verbose=False, quiet=True)
        shprint(ctx, msg='Generated flamegraph:')
        out_local_path = 'file://{}'.format(paths.base('.container/profiler/{}'.format(filename)))
        if not dev_tools:
            shprint(ctx, msg='  Access in browser at {}'.format(out_local_path))
            if os.path.isdir('/Applications/Google Chrome.app'):
                ctx.run('open -a "/Applications/Google Chrome.app" \'{}\''.format(out_local_path))
        if dev_tools:
            shprint(ctx, msg='  Load the generated cpuprofile in chrome dev tools {}'.format(out_local_path))
    except Exception as e:
        shprint(ctx, msg='Looks like there was a problem. Check the help method to make sure you have everything configured.', color='yellow')
        shprint(ctx, msg='    invoke -h test.profile', color='yellow')


@task
def coverage(ctx, modules, db=''):
    """
    Run coverage tests.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param modules {str}:
    :param db {str}:
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.test_coverage(ctx, modules, db)
