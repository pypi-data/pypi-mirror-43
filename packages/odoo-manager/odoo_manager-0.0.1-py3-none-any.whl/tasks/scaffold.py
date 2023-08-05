import os
from invoke import task
from .lib.shell import shprint
from .lib.tasks import Tasks
from .lib import paths as path_helpers
from .lib.helpers import redirect

paths = path_helpers.Paths()


@task
def tests(ctx, module, verbose=False):
    """
    Generate a testing scaffold for a given module.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param module {str}: The name of the module to generate a test scaffold for
    :param verbose {bool}:
    :return {NoneType}:
    """
    if not os.path.isdir(paths.base(module)):
        shprint(ctx, msg='The module {} is not a valid module.'.format(module), color='red')
        exit(1)

    Tasks.setup(ctx)
    tests_dir = paths.base(os.path.join(module, 'tests'))
    test_type_dirs = [('components', os.path.join(tests_dir, 'component')),
                      ('security', os.path.join(tests_dir, 'security')),
                      ('structural', os.path.join(tests_dir, 'structural')),
                      ('use_case', os.path.join(tests_dir, 'use_case')), ]

    shprint(ctx, msg='Checking tests dir...')
    if not os.path.isdir(tests_dir):
        ctx.run('mkdir {}{}'.format(tests_dir, redirect(verbose)))
    if not os.path.isfile(os.path.join(tests_dir, '__init__.py')):
        ctx.run('touch {}{}'.format(os.path.join(tests_dir, '__init__.py'), redirect(verbose)))

    for test_type, test_type_dir in test_type_dirs:
        init_path = os.path.join(test_type_dir, '__init__.py')
        shprint(ctx, msg='  *Checking {} tests...'.format(test_type))
        if not os.path.isdir(test_type_dir):
            ctx.run('mkdir {}{}'.format(test_type_dir, redirect(verbose)))
        if not os.path.isfile(init_path):
            ctx.run('touch {}{}'.format(init_path, redirect(verbose)))
    shprint(ctx, msg='Tests scaffolding generated.')
