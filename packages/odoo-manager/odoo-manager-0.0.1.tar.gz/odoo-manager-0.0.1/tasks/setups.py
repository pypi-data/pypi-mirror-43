import json
import os
import getpass
import sys
import shutil
import filecmp
import requests
import jinja2
from invoke import task
from invoke.exceptions import UnexpectedExit

from .lib import configs
from .lib import database
from .lib import validation
from .lib import paths as path_helpers
from .lib.tasks import Tasks
from .lib.shell import shprint

pipe_dev_null = path_helpers.pipe_dev_null
paths = path_helpers.Paths()


@task(default=True)
def setup(ctx, odoo_version='', verbose=False, validate=True, git=True):
    """
    Build out the tool set, locally, for this collection.

    This is mainly used to setting up the tools that we are going to use for
    development. It does not setup the application itself. That will be handled
    from the `build` task.

    1. Runs `git pull` to ensure .om is up to date
    2. Copies tasks.py to the root of this project for `invoke` to work

    :param ctx {invoke.context.Context}: Invoke context variable
    :param odoo_version:
    :return {NoneType}:
    """
    Tasks.setup(ctx, odoo_version, verbose, validate, git)


@task
def mapping(ctx, path):
    """
    Update the docker-compose.yml file with the correct module mapping.

    :param path:
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.setup_mapping(ctx, path)


@task(aliases=('depends', ))
def dependencies(ctx, noupdate=False, only='', setup=True, git=True, yes=False, ls=False):
    """
    Install third party dependencies based on the module manifest.

    :return {NoneType}:
    """
    if setup:
        Tasks.setup(ctx, git=git)

    if ls:
        all_dependencies = set()
        current_modules = set()
        missing_modules = set()
        core_modules = _get_core_addons()

        to_process = Tasks.details(ctx, 'all', names=True, custom_only=True, pretty=False, prints=False)
        for module in to_process:
            module_config_path = False
            potential_paths = (paths.base('{}/__openerp__.py'.format(module)),
                               paths.base('_lib/{}/__openerp__.py'.format(module)),
                               paths.base('_lib_static/{}/__openerp__.py'.format(module)),
                               paths.base('{}/__manifest__.py'.format(module)),
                               paths.base('_lib/{}/__manifest__.py'.format(module)),
                               paths.base('_lib_static/{}/__manifest__.py'.format(module)), )

            for potential_path in potential_paths:
                if os.path.isfile(potential_path):
                    module_config_path = potential_path
                    break

            if module_config_path:
                all_dependencies.add(module)
                current_modules.add(module)
                with open(module_config_path) as config_file:
                    config = eval(config_file.read())
                    if 'depends' in config:
                        for dependency in config['depends']:
                            all_dependencies.add(dependency)

        shprint(ctx, msg='\nAll Depedencies\n' + ('=' * 15), color='lightblue')
        for dependency in sorted(all_dependencies):
            if dependency not in core_modules:
                if dependency not in current_modules:
                    missing_modules.add(dependency)
                shprint(ctx, msg='  - {}'.format(dependency), color='lightblue')
        shprint(ctx, msg='')

        if missing_modules:
            shprint(ctx, msg='Missing Modules\n' + ('=' * 15), color='yellow')
            for dependency in sorted(missing_modules):
                shprint(ctx, msg='  - {}'.format(dependency), color='yellow')
            shprint(ctx, msg='')
    else:
        Tasks.setup_dependencies(ctx, noupdate, only, yes)


def _get_core_addons():
    addons = set()
    check_directories = ['.container/core/addons',
                         '.container/core/odoo/addons',
                         '.container/core/openerp/addons',
                         '.container/enterprise', ]
    for path in check_directories:
        if os.path.isdir(paths.base(path)):
            addons.update(os.listdir(paths.base(path)))
    return addons


@task
def version(ctx, odoo_version):
    """
    Check the current version of odoo or set the version of odoo.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param odoo_version:
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.version(ctx, odoo_version)
