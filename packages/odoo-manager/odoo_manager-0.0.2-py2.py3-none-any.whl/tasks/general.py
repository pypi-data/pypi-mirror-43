import os
import re
import json
import getpass
import unicodedata
from invoke import Collection, task

from . import setups
from .lib import configs
from .lib import validation
from .lib import paths as path_helpers
from .lib.tasks import Tasks
from .lib.shell import shprint

try:
    import networkx as network
    from asciinet import graph_to_ascii
except:
    network = False
    graph_to_ascii = False

pipe_dev_null = path_helpers.pipe_dev_null
paths = path_helpers.Paths()


@task(aliases=('stop', ))
def down(ctx):
    """
    Stop and remove the current docker containers for this project.

    :param ctx {invoke.context.Context}: Invoke context variable
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.down(ctx)


@task
def build(ctx, update=False, only_docker=False, only_odoo=False, no_pip=False, no_depends=False, no_cache=False, verbose=False, setup=True):
    """
    Builds the requirements to run the project inside the docker environment.

    This will setup any required files, and run any listed setup scripts. This
    is focused specifically on building out the project environment. See the
    `setup` command for reference to setting up the development tools.

    1. Runs the build/setup processes to setup the Odoo source
    2. Runs the update processes to update the Odoo source (if the --update flag
       is passed)

    :param ctx {invoke.context.Context}: Invoke context variable
    :param update {bool}:
    :param only_docker {bool}:
    :param only_odoo {bool}:
    :param no_pip {bool}:
    :param no_depends {bool}:
    :param no_cache {bool}:
    :param verbose {bool}:
    :return {NoneType}:
    """
    if setup:
        Tasks.setup(ctx, validate=False)
    Tasks.build(ctx, update, only_docker, only_odoo, no_pip, no_depends, no_cache, verbose)


@task
def dockerize(ctx):
    Tasks.setup(ctx)
    shprint(ctx, msg='Coming soon.')


@task
def createdb(ctx, database, demo=False, init=''):
    """
    Create a database with or without demo data and modules.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param database {str}: name of the database to create
    :param demo {bool}: determines if demo data should be installed
    :param init {str}: comma-separated string of modules to install
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.createdb(ctx, database, demo, init)


@task
def upgrade(ctx):
    """
    Upgrade the tool set locally to use the latest code.

    TODO

    :param ctx {invoke.context.Context}: Invoke context variable
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.upgrade(ctx)


@task
def ps(ctx, all=False):
    """
    Show the docker containers running.

    :param ctx {invoke.context.Context}: Invoke context variable
    :return {NoneType}:
    """
    if not all:
        ctx.run('docker-compose ps')
    else:
        ctx.run('docker ps')


@task
def ssh(ctx, container, cmd=False, executable='', verbose=False):
    """
    SSH into the current Docker container running.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param container {str}:
    :param cmd {bool}:
    :param executable {str}:
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.ssh(ctx, container, cmd, executable, verbose, quiet=False)


@task
def restart(ctx, container='web', verbose=False):
    """
    Restart a specific container.

    This is primarily used to restart Odoo. This is helpful during development
    to use instead of stopping and starting the entire container every single
    time.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param container {str}:
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.restart(ctx, container, verbose)


@task
def debug(ctx, container='web', verbose=False):
    """
    Attach to a container to see the pdb or ipdb shell.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param container {str}:
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.attach(ctx, container, verbose)


@task
def attach(ctx, container='web', verbose=False):
    """
    Attach to a container.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param container {str}:
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.attach(ctx, container, verbose)


@task
def log(ctx, grep=''):
    """
    Tail the logs for the current Docker container running.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param grep {str}:
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.log(ctx, grep)


@task
def logs(ctx, grep=''):
    """
    Alias for log.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param grep {str}:
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.log(ctx, grep)


@task
def psql(ctx, db=''):
    """
    Open up the psql shell.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param db {str}:
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.psql(ctx, db)


@task
def docs(ctx):
    """
    Build and display html Sphinx documentation.

    :param ctx {invoke.context.Context}: Invoke context variable
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.docs(ctx)


@task
def clean(ctx, rm=False):
    """
    Clean the repository in preparation for production deployment.

    1. Remove any unneeded modules (given the --rm flag)
    2. Prompt the user to update static files on all modules (images,
       docs/boilerplate, manifest details, etc.)
    3. Prompt the user for styling/linting

    :param ctx {invoke.context.Context}: Invoke context variable
    :param rm {bool}:
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.clean(ctx, rm)


@task
def style(ctx):
    """
    Reformat all of the files in the repo to match our code style.

    :param ctx {invoke.context.Context}: Invoke context variable
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.style(ctx)


@task
def lint(ctx):
    """
    Lint all the py files using pylint and check for common Odoo mistakes.

    Pylint will handle linting for syntax and structure of the code, and our
    custom tools will handling linting each module for common Odoo mistakes such
    as missing security files, use of deprecated method, etc.

    :param ctx {invoke.context.Context}: Invoke context variable
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.lint(ctx)


@task
def new_module(ctx, branch='', name='', verbose=False):
    """
    Generate a new Odoo module.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param branch:
    :param name:
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.new_module(ctx, branch, name, verbose)


@task
def image(ctx, project, username, image, tag, push=False):
    """
    Generate a new Docker image for this project.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param project {str}:
    :param username {str}:
    :param image {str}:
    :param tag {str}:
    :param push {bool}:
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.image(ctx, project, username, image, tag, push)


@task
def details(ctx, module='', names=False, custom_only=False, pretty=False, setup=True):
    """
    Print details about a specific module or list of modules.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param module {str}: Name of a module to get details about
    :param names {bool}: True if you only want the names of modules
    :param custom_only {bool}:
        True if you only want to reference custom modules created by blue
        stingray developers.
    :param pretty {bool}: True if you want to pretty print names
    :return {NoneType}:
    """
    if setup:
        Tasks.setup(ctx)
    Tasks.details(ctx, module, names, custom_only, pretty)


@task
def graph(ctx, modules=''):
    """
    Print a dependency graph of a single module or list of modules.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param module {str}: Name of a module or modules to print a graph for
    :return {NoneType}:
    """
    if not graph_to_ascii:
        return shprint(ctx, 'Install asciinet from https://github.com/cosminbasca/asciinet.', color='pink')

    to_process = Tasks.details(ctx, 'all', names=True, custom_only=True, pretty=False, prints=False)
    if modules:
        to_process = modules.split(',')

    Tasks.setup(ctx)

    dependency_graph = network.Graph()
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
            if module not in dependency_graph.nodes:
                dependency_graph.add_node(module)
            with open(module_config_path) as config_file:
                config = eval(config_file.read())
                if 'depends' in config:
                    for dependency in config['depends']:
                        if dependency not in dependency_graph.nodes:
                            dependency_graph.add_node(dependency)
                        dependency_graph.add_edge(module, dependency)
        else:
            shprint(ctx, msg='Could not find manifest or openerp for module {}'.format(module), color='yellow')

    graph_ascii = graph_to_ascii(dependency_graph)
    rows = graph_ascii.split('\n')
    for row in rows:
        shprint(ctx, msg=row, color='lightgrey')


@task
def deploy(ctx):
    """
    Deploy the application to either a quality, staging, or production server.

    :param ctx {invoke.context.Context}: Invoke context variable
    :return {NoneType}:
    """
    Tasks.setup(ctx)
    Tasks.deploy(ctx)


@task
def mkdocs(ctx, template_dir=".templates/"):
    """
    If there is a 'template_dir' (default=.templates) will generate Odoo App
    page documentation.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param template_dir {str}:
    :return:
    """
    Tasks.mkdocs(ctx, template_dir)
