import json
import os
import getpass
import sys
import shutil
import filecmp
import time
import io
import requests
import jinja2
import imp
import re
import random
import string

from . import configs
from . import validation
from . import paths as path_helpers
from . import database
from .shell import shprint
from .helpers import redirect, clean_test_dir, cleanup, env, update_dependency, diff_dependency, \
    diff_dependency_git, git_clone, print_diff_files, parse_config, console_colors, _get_container_sh_cmd, \
    _get_container_exec_cmd, _get_container_id_cmd, _iterate_py_files, _check, _mkdoc_get_context, _mkdoc_get_templates, \
    _mkdoc_render

from invoke import task
from invoke.exceptions import UnexpectedExit

pipe_dev_null = path_helpers.pipe_dev_null
paths = path_helpers.Paths()

# We are going to define are constants for environments so we can change the
# behavior of the program depending on the envioronment. Developers will
# actually get the environment through the env() function defined in this file,
# and the environment variable will be pulled from the .env file in the root
# directory of the project.
#
# We are going to default envionemnt to development if not defined in the .env
# but we expect the following uses for each type:
#
#   - production: Used for deploying the application on production servers
#   - development: Used for local environments where a developer is working on
#     the project
#   - tools: Used for modifying the .om or .om/collections tools
ENV_PRODUCTION = 'production'
ENV_DEVELOPMENT = 'development'
ENV_TOOLS = 'tools'

YES_OPTIONS = ('y', 'ye', 'yes', 'ya')


class Tasks(object):

    @staticmethod
    def run(ctx, rebuild=False, update=False, args='', detach=False, compose='', verbose=False):
        validation.check_env(configs.config, ['PIP_EXE', 'ODOO_EXE', 'LOCAL_PORT'])

        if rebuild:
            Tasks.build(ctx, update=update, verbose=verbose)

        if args and ('-i' in args or '--install' in args or '-u' in args or '--upgrade' in args) and ('-d' not in args and '--database' not in args):
            print('Make sure you include the -d flag when trying to upgrade or install modules.')
            exit(1)

        if not compose:
            compose = 'docker-compose.yml'

        # We are going to rewrite args every time no matter if it was passed
        # in or not. We don't want to run into a situation where a user uses
        # args once, and then has the same flags passed in over and over since
        # the odoo.env file will be written.
        #
        # If the user passes in args, then the next time does not, we should
        # assume we need to write an empty string to the odoo.env.
        if configs.config.has_option('options', 'ODOO_FLAGS'):
            try:
                ctx.run("sed -i '' '/^ODOO_FLAGS/d' {}{}".format(configs.standard_env_path, redirect(verbose)))
            except:
                ctx.run("sed -i '/^ODOO_FLAGS/d' {}{}".format(configs.standard_env_path, redirect(verbose)))
        if configs.odoo_env_config.has_option('options', 'ODOO_FLAGS'):
            try:
                ctx.run("sed -i '' '/^ODOO_FLAGS/d' {}{}".format(configs.odoo_env_path, redirect(verbose)))
            except:
                ctx.run("sed -i '/^ODOO_FLAGS/d' {}{}".format(configs.odoo_env_path, redirect(verbose)))

        shprint(ctx, msg='Running project...')
        if not verbose:
            shprint(ctx, msg='You are not running in verbose mode, so container logs/output will not appear here. Tail '
                             'logs or run this command with the --verbose flag to see output. It may take a minute for '
                             'all containers to fully start.', color='yellow')
        shprint(ctx, msg='  detach?: {}'.format(detach), color='lightgrey')
        shprint(ctx, msg='  args:    {}'.format(args or 'None'), color='lightgrey')
        shprint(ctx, msg='  port:    {}'.format(configs.config.get('options', 'LOCAL_PORT')), color='lightgrey')
        shprint(ctx, msg='  url:     http://localhost:{}'.format(configs.config.get('options', 'LOCAL_PORT')), color='lightgrey')

        try:
            ctx.run("echo 'ODOO_FLAGS={}' >> {}".format(args, configs.odoo_env_path))
            ctx.run('docker-compose -f {} up {}{}'.format(compose, '-d' if detach else '', redirect(verbose)))
        except UnexpectedExit as e:
            # Handle the unexpected exit while trying to run docker-compose up.
            # There are a couple of scenarios. We only care about an error code
            # "1" coming back which means that our program died on it's own. We
            # do not care about the user stopping the command with a ctrl-c
            # input.
            if e.result.exited == 1:
                shprint(ctx, msg='There was a problem running docker-compose.{}'.format(
                    ' Try again with --verbose to see the error information.' if not verbose else ''), color='pink')

    @staticmethod
    def down(ctx):
        shprint(ctx, msg='Stopping containers...')
        ctx.run('docker-compose stop{}'.format(redirect(verbose=False)))
        shprint(ctx, msg='Containers stopped.')

    @staticmethod
    def setup(ctx, odoo_version='', verbose=False, validate=True, git=True):
        """
        The method that is run on almost every invoke command to ensure that
        the local toolset has everything that it should, and to make sure that
        what it currently has is up to date.
        """
        can_setup = configs.can_setup()
        configs.setup_called()
        if not can_setup:
            return

        if not configs.config or not configs.odoo_env_config:
            shprint(ctx, msg='WARNING: Please configure an .env file. You may have issues when trying to build or run without one.',
                    color='yellow')

        if validate:
            validation.check_packages(ctx)

        shprint(ctx, msg='Setting up...', run=verbose)
        if os.path.isfile(paths.base('.om/tasks/__init__.py')):
            def update_git_repo(repo_name, repo_path, check_file, environment):
                try:
                    if environment == ENV_TOOLS:
                        shprint(ctx, msg='WARN: Not pulling {} because you are in tools mode.'.format(repo_name), color='yellow')
                    else:
                        if os.path.isfile(check_file):
                            ctx.run('cd {} && git pull{}'.format(repo_path, redirect(verbose)))
                        else:
                            shprint(ctx, msg='Missing {} directory. You may need to run make.sh before trying to use invoke.'.format(repo_name),
                                    color='pink')
                except Exception as e:
                    shprint(ctx, msg='WARN: Could not pull the git repository for {}'.format(repo_name), color='yellow')
                    if verbose:
                        shprint(ctx, msg=str(e), color='yellow')

                    shprint(ctx, msg='There may be changes in the {} repo locally'.format(repo_name), color='yellow')
                    if input('Would you like you stash those changes and reset to origin/master (y/n)? ').lower() in YES_OPTIONS:
                        shprint(ctx, msg='  *Resetting {} to origin/master.'.format(repo_name))
                        try:
                            ctx.run('cd {} && git stash && git checkout master && git reset --hard origin/master{}'.format(repo_path, redirect(verbose)))
                            shprint(ctx, msg='  *Reset {}.'.format(repo_name))
                        except Exception as e:
                            shprint(ctx, msg='There was a problem resetting {}. Review and try running this command again'.format(repo_name),
                                    color='pink')
                            if verbose:
                                ctx.run(ctx, msg=str(e), color='yellow')
                    else:
                        shprint(ctx, msg='Please review the repo in {} for changes and try running this command again'.format(repo_name),
                                color='yellow')
                        exit(1)

            # First we are going to try to update the sub repos that we have
            # stored in the project directory. If there is a problem doing a git
            # pull then it most likely just means that you have there internet
            # access or the remote git server is non responsive, but we will
            # also check for local change in the repo.
            if git:
                shprint(ctx, msg='  *Checking .om and .om/collections...', run=verbose)

                update_git_repo(repo_name='.om',
                                repo_path=paths.base('.om'),
                                check_file=paths.base('.om/tasks/__init__.py'),
                                environment=env())
                update_git_repo(repo_name='.om/collections',
                                repo_path=paths.base('.om/collections'),
                                check_file=paths.base('.om/collections/make.sh'),
                                environment=env())

            shprint(ctx, msg='  *Copying tasks and make.sh to root...', run=verbose)
            if not os.path.isfile(paths.base('tasks/__init__.py')):
                ctx.run('ln -s {} {}'.format(paths.base('.om/tasks'), paths.base('tasks')))
            elif os.path.isfile(paths.base('tasks.py')):
                # If it is already symlinked then we can force cleanup of the
                # tasks.py file
                ctx.run('rm {}'.format(paths.base('tasks.py')))
            if os.path.isfile(paths.base('.om/collections/make.sh')):
                ctx.run('cp {} {}'.format(paths.base('.om/collections/make.sh'), paths.base('make.sh')))

            shprint(ctx, msg='  *Copying requirements.txt to root...', run=verbose)
            ctx.run('cp {} {}'.format(paths.base('.om/collections/requirements.txt'), paths.base('requirements.txt')))

        Tasks._setup_drone(ctx, odoo_version, verbose, validate, git)
        Tasks._setup_linting(ctx, verbose)
        shprint(ctx, msg='', run=verbose)
        if odoo_version:
            version(ctx, odoo_version)

    @staticmethod
    def _setup_drone(ctx, odoo_version='', verbose=False, validate=True, git=True):
        """
        Helper method to configure the .drone.yml file within the current
        project.
        """
        shprint(ctx, msg='  *Copying .drone.yml to root...', run=verbose)
        shprint(ctx, msg='    *Checking pipeline configuration...', color='lightgrey', run=verbose)

        pipeline_conf_path = paths.base('.pipeline/pipeline.conf')
        if os.path.isfile(pipeline_conf_path):
            configuration = configs.load_standard_config(pipeline_conf_path)
            if configuration:
                def _check_configs(data, required):
                    for check in required:
                        fields = check.split('.')
                        val = data[fields[0]]
                        if len(fields) > 1:
                            for field in fields[1:]:
                                val = val[field]
                        if not val:
                            return False
                    return True

                def _get_option(key, default=None):
                    if configuration.has_option('options', key):
                        return configuration.get('options', key)
                    return default

                pipelineconf = {'channel': _get_option('drone_channel'),
                                'hook': _get_option('drone_hook'),
                                'deploy': True if _get_option('deploy', 'False') == 'True' else False,
                                'deploy_options': {'secret': _get_option('deploy_secret', '').upper(),
                                                   'project': _get_option('deploy_project', False),
                                                   'instance': _get_option('deploy_instance', False),
                                                   'zone': _get_option('deploy_zone', False),
                                                   'path': _get_option('deploy_path', '/odoo/builds').strip('/'),
                                                   'branches': _get_option('deploy_branches', 'development'), }}

                # Check and make sure that the user has passed all of the proper
                # pipeline options.
                if not _check_configs(pipelineconf, ['channel', 'hook']):
                    shprint(ctx, color='yellow', msg='WARN: Your .pipeline/pipeline.conf should have a drone_channel and drone_hook.')
                    return
                if pipelineconf['deploy']:
                    if not _check_configs(pipelineconf, ['deploy_options.secret',
                                                         'deploy_options.project',
                                                         'deploy_options.instance',
                                                         'deploy_options.zone']):
                        shprint(ctx, color='yellow', msg='WARN: Your .pipeline/pipeline.conf does not have the proper deployment configurations.')
                        return
                    for branch in pipelineconf['deploy_options']['branches'].split(','):
                        if not os.path.isfile(paths.base('.pipeline/configs/env/.env.{}'.format(branch))):
                            shprint(ctx, color='yellow', msg='WARN: Make sure that you have .env files for each deployable branch.')
                            return

                shprint(ctx, msg='    *Building .drone.yml...', color='lightgrey', run=verbose)
                try:
                    ctx.run('cp {} {}'.format(paths.base('.om/.drone.yml'), paths.base('.drone.yml')))
                    with open(paths.base('.drone.yml'), 'r+') as drone_file:
                        contents = drone_file.read()
                        contents = contents.replace('{{ pipeline.drone_channel }}', pipelineconf['channel'])
                        contents = contents.replace('{{ pipeline.drone_hook }}', pipelineconf['hook'])

                        if not pipelineconf['deploy']:
                            start = contents.index('{{ if deploy }}')
                            stop = contents.index('{{ endif deploy }}') + 19  # Adding the length of the endif statement plus 1 line of padding
                            contents = contents[0:start] + contents[stop:]
                        else:
                            contents = contents.replace('{{ if deploy }}', '')
                            contents = contents.replace('{{ endif deploy }}', '')
                            contents = contents.replace('{{ pipeline.deploy.project }}', pipelineconf['deploy_options']['project'])
                            contents = contents.replace('{{ pipeline.deploy.zone }}', pipelineconf['deploy_options']['zone'])
                            contents = contents.replace('{{ pipeline.deploy.instance }}', pipelineconf['deploy_options']['instance'])
                            contents = contents.replace('{{ pipeline.deploy.secret }}', pipelineconf['deploy_options']['secret'])
                            contents = contents.replace('{{ pipeline.deploy.path }}', pipelineconf['deploy_options']['path'])

                            branch_str = ''
                            for i, branch in enumerate(pipelineconf['deploy_options']['branches'].split(',')):
                                branch_str += ((' ' * 8) if i > 0 else '') + "- {}*\n".format(branch)
                            contents = contents.replace('{{ pipeline.deploy.branches }}', branch_str)

                        drone_file.seek(0)
                        drone_file.truncate()
                        drone_file.write(contents)
                except Exception as e:
                    shprint(ctx, color='yellow', msg='WARN: Your .drone.yml did not update properly because there was a problem inserting '
                                                     'variables into your .drone.yml file.')
                    shprint(ctx, msg=str(e), color='pink', run=verbose)
            else:
                shprint(ctx, color='yellow', msg='WARN: Your .drone.yml did not update properly because there was a problem parsing your '
                                                 '.pipeline/pipeline.conf.')
        else:
            shprint(ctx, msg='WARN: Your .drone.yml did not update properly because you do not have a valid .pipeline/pipeline.conf', color='yellow')

    @staticmethod
    def _setup_linting(ctx, verbose=False):
        """
        Helper method to configure the linter and pre-commit files within the
        current project.
        """
        if not configs.config.has_option('options', 'LINT') or configs.config.get('options', 'LINT') == '1':
            shprint(ctx, msg='  *Copying linter files to root...', run=verbose)
            if not os.path.isfile(paths.base('.pre-commit-config.yaml')):
                ctx.run('ln -s {} {}'.format(paths.base('.om/.pre-commit-config.yaml'), paths.base('.pre-commit-config.yaml')))
            if not os.path.isfile(paths.base('.pydocstyle')):
                ctx.run('ln -s {} {}'.format(paths.base('.om/.pydocstyle'), paths.base('.pydocstyle')))
            if not os.path.isfile(paths.base('.pylintrc')):
                ctx.run('ln -s {} {}'.format(paths.base('.om/.pylintrc'), paths.base('.pylintrc')))
            if ctx.run('which pre-commit'):
                shprint(ctx, msg='  *Installing pre-commit...', run=verbose)
                ctx.run('pre-commit install')
            else:
                shprint(ctx, msg='  ***pre-commit is not installed! Install it with pip3***')

    @staticmethod
    def setup_mapping(ctx, path):
        print('Coming soon')

    @staticmethod
    def setup_dependencies(ctx, noupdate=False, only='', yes=False):
        """
        :param bool noupdate: (optional) if True, only non-existent modules
                              will be updated
        :param str only: (optional) comma-separated string used to only update
                         specific modules
        :return None:
        """
        configuration = parse_config()
        cleanup()

        shprint(ctx, msg='Setting up project dependencies...')
        if 'depends' in configuration:
            effected_modules = []
            problem_modules = []
            dependencies = only.split(',') if only else configuration['depends']
            for dependency_name in dependencies:
                if not noupdate or (noupdate and not os.path.isdir(paths.base('_lib/{}'.format(dependency_name)))):
                    effected_modules.append(dependency_name)
                    diff_dependency(ctx, dependency_name, configuration['depends'][dependency_name])

            if problem_modules:
                shprint(ctx, msg='The following modules had some problem ...', color='lightred')
                shprint(ctx, msg='  ' + str.join("\n  ", problem_modules), color='lightgrey')

            if effected_modules:
                shprint(ctx, msg='')
                shprint(ctx, msg='Adding the following modules to _lib...', color='lightblue')
                shprint(ctx, "\n---\n", color='lightblue')
                shprint(ctx, msg='  ' + str.join("\n  ", effected_modules), color='lightgrey')
                shprint(ctx, "\n---\n", color='lightblue')

                if yes or str(input('Review any diffs above. Should we continue to overwrite? This will overwrite the _lib modules listed above with files '
                                    'from the dependency source (y/n) :')).lower() in YES_OPTIONS:
                    for dependency_name in effected_modules:
                        update_dependency(ctx, dependency_name, configuration['depends'][dependency_name])
                shprint(ctx, msg='\nAll done.')
            else:
                shprint(ctx, msg='\nEverything up to date.')

        cleanup()

    @staticmethod
    def version(ctx, odoo_version):
        supported_versions = ['9.0', '10.0', '11.0']

        if odoo_version not in supported_versions:
            shprint(ctx, msg='The version {} is not currently supported. Use one of the following: {}'.format(
                odoo_version, ', '.join(supported_versions)))
            exit()

        if odoo_version == '9.0':
            shprint(ctx, msg='Setting up version 9.0...')
            shprint(ctx, msg='Coming soon')

        if odoo_version == '10.0':
            shprint(ctx, msg='Setting up version 10.0...')
            shprint(ctx, msg='Coming soon')

        if odoo_version == '11.0':
            shprint(ctx, msg='Setting up version 11.0...')
            shprint(ctx, msg='Coming soon')

    @staticmethod
    def build(ctx, update=False, onlydocker=False, onlyodoo=False, nopip=False, nodepends=False, nocache=False, verbose=False):
        validation.check_env(configs.config, ['ODOO_VERSION', 'USE_ENTERPRISE', 'GIT_DEPTH'])

        shprint(ctx, msg='Running build process...')

        if not nopip:
            shprint(ctx, msg='  *Install pip3 requirements...')
            ctx.run('pip3 install --user --quiet -r {}'.format(paths.base('requirements.txt')))

        if not onlyodoo:
            shprint(ctx, msg='  *Building docker image with docker-compose build...')
            ctx.run('docker-compose build{}{}'.format(' --no-cache' if nocache else '', redirect(verbose)))

        if not onlydocker:
            shprint(ctx, msg='  *Making directories...')
            if not os.path.isdir(paths.base('.container/testresults')):
                ctx.run('mkdir -p {}'.format(paths.base('.container/testresults')))

            if update:
                # If using the --update flag then we are going to force an
                # update of the current Odoo source.
                # TODO.
                pass
            else:
                # If there is no --update flag then we are going to assume that
                # the user wants to run a standard build process.

                odoo_version = configs.config.get('options', 'ODOO_VERSION')
                use_enterprise = configs.config.get('options', 'USE_ENTERPRISE') != '0'
                depth = configs.config.get('options', 'GIT_DEPTH')

                shprint(ctx, msg='  *Installing odoo source...')
                shprint(ctx, msg='      odoo version:      {}'.format(odoo_version), color='lightgrey')
                shprint(ctx, msg='      using enterprise?: {}'.format(use_enterprise), color='lightgrey')
                shprint(ctx, msg='      repo depth:        {}'.format(depth), color='lightgrey')
                shprint(ctx, msg='', color='lightgrey')

                if not os.path.isdir(paths.base('.container/core/addons')):
                    if os.path.isdir(paths.base('.container/core')):
                        shprint(ctx, msg='      Cleaning up existing core folder...')
                        ctx.run('rm -rf {}'.format(paths.base('.container/core')))
                    shprint(ctx, msg='      Cloning down repo from github.com/odoo/odoo...')
                    git_clone(ctx, 'https://github.com/odoo/odoo', odoo_version, 'odoo/odoo',
                              output=paths.base('.container/core'), depth=depth)

                # Do some additional cleanup on core for missing JS files.
                us_locale_path = paths.base('.container/core/addons/web/static/lib/moment/locale/en-us.js')
                ca_locale_path = paths.base('.container/core/addons/web/static/lib/moment/locale/en-ca.js')
                if not os.path.isfile(us_locale_path) and os.path.isfile(ca_locale_path):
                    shprint(ctx, msg='  *Cleaning up moment locales...')
                    ctx.run('cp {} {}'.format(ca_locale_path, us_locale_path))

                # TODO: Make sure that if an incorrect password is used that it
                # gives feedback
                if use_enterprise:
                    if not os.path.isdir(paths.base('.container/enterprise/account_reports')):
                        if os.path.isdir(paths.base('.container/enterprise')):
                            shprint(ctx, msg='      Cleaning up existing enterprise folder...')
                            ctx.run('rm -rf {}'.format(paths.base('.container/enterprise')))
                        shprint(ctx, msg='      Cloning down repo from github.com/odoo/enterprise...')
                        git_clone(ctx, 'https://github.com/odoo/enterprise', odoo_version, 'odoo/enterprise',
                                  output=paths.base('.container/enterprise'), depth=depth)

    @staticmethod
    def createdb(ctx, database, demo=False, init=''):
        args = "-d {database}".format(database=database)
        if init:
            args += " -i {init}".format(init=init)
        if not demo:
            args += " --without-demo=all"
        run(ctx, args=args)

    @staticmethod
    def upgrade(ctx):
        pass

    @staticmethod
    def ssh(ctx, container, cmd=False, executable='', verbose=False, quiet=True):
        basename = os.path.basename(os.path.realpath(paths.base('.'))).replace(' ', '')

        try:
            try:
                ssh_cmd = 'docker exec -it $(docker ps -q --filter name={base}_{container}) sh'.format(
                    base=basename, container=container)
                ctx.run(ssh_cmd, pty=True)
            except:
                ssh_cmd = 'docker exec -it $(docker ps -q --filter name={base}_{container}) sh'.format(
                    base=basename.replace('_', ''), container=container)
                ctx.run(ssh_cmd, pty=True)
        except UnexpectedExit as e:
            if e.result.exited == 1:
                shprint(ctx, color='pink',
                        msg='There was a problem running docker exec. Make sure that the containers that you are trying to access are '
                            'currently running.{}'.format(' Try again with --verbose to see the error information.' if not verbose else ''))

    @staticmethod
    def restart(ctx, container='web', verbose=False):

        try:
            shprint(ctx, msg='Restarting containers...')
            if not container or container == 'all':
                shprint(ctx, msg='  *Restarting all containers')
                ctx.run('docker-compose restart{}'.format(redirect(verbose)))
            else:
                shprint(ctx, msg='  *Restarting container {}'.format(container))
                ctx.run('docker-compose restart {}{}'.format(container, redirect(verbose)))
            shprint(ctx, msg='Containers restarted.')
        except UnexpectedExit as e:
            if e.result.exited == 1:
                shprint(ctx, msg='There was a problem restarting the docker containers.{}'.format(
                    ' Try again with --verbose to see the error information.' if not verbose else ''), color='pink')
            exit(1)

    @staticmethod
    def attach(ctx, container='web', verbose=False):
        basename = os.path.basename(os.path.realpath(paths.base('.'))).replace(' ', '')
        shprint(ctx, msg='Attaching to container {}'.format(container))
        shprint(ctx, msg='  *Checking that docker-compose is setup properly')

        try:
            error = False
            with open(paths.base('docker-compose.yml')) as f:
                compose_contents = f.read()
                if '{}:'.format(container) not in compose_contents:
                    error = 'Your docker-compose.yml does not have the container {} defined.'.format(container)
                if 'stdin_open: true' not in compose_contents or 'tty: true' not in compose_contents:
                    error = 'Your docker-compose.yml is not configured for debuggers. Ensure that your container {} has the following defined:'.format(
                        container)
                    error += '\n  {}:'.format(container)
                    error += '\n    stdin_open: true'
                    error += '\n    tty: true'

            if error:
                shprint(ctx, msg=error, color='pink')
                exit()
        except Exception as e:
            shprint(ctx, msg='There was a problem accessing your docker-compose.yml file.', color='pink')
            exit()

        try:
            shprint(ctx, msg='\nRunning attach command now. You will be attached to the container if successful and will start with a '
                             'blank prompt.\n\nTo exit, please use ctrl-c.\n\nIf you are expecting a pdb prompt press enter to check if '
                             'pdb is currently triggered.', color='yellow')

            try:
                ctx.run('docker attach --detach-keys="ctrl-c" $(docker ps -q --filter name={base}_{container})'.format(
                    base=basename, container=container), pty=True)
            except:
                ctx.run('docker attach --detach-keys="ctrl-c" $(docker ps -q --filter name={base}_{container})'.format(
                    base=basename.replace('_', ''), container=container), pty=True)
        except UnexpectedExit as e:
            if e.result.exited == 1 and 'read escape sequence' not in str(e.result):
                shprint(ctx, msg='There was a potentially a problem running docker attach. Make sure that the containers that you are '
                                 'trying to access are currently running.', color='pink')
        except ProgrammingError as e:
            shprint(ctx, msg='Exiting.', color='pink')
            Tasks.restart(ctx, container)

    @staticmethod
    def run_shell(ctx, db, container='web'):
        found_executable = False
        container_odoo_path = '/opt/odoo/core'
        local_odoo_path = paths.base('.container/core')
        odoo_executables = ['odoo-bin', 'openerp-server']

        for executable in odoo_executables:
            if os.path.isfile('{}/{}'.format(local_odoo_path, executable)):
                found_executable = True
                cmd = 'docker-compose run {} {}/{} shell -c /opt/odoo/config/odoo.conf --xmlrpc-port=8888 --longpolling-port=8899 -d {}'.format(
                    container, container_odoo_path, executable, db)
                ctx.run(cmd, pty=True)
                break

        if not found_executable:
            shprint(ctx, msg='There was a problem finding the odoo executable', color='pink')
            exit(1)

    @staticmethod
    def log(ctx, grep=''):

        if grep:
            cmd = 'tail -f {} | grep {}'.format(paths.base('.container/log/odoo.log'), grep)
        else:
            cmd = 'tail -f {}'.format(paths.base('.container/log/odoo.log'))

        ctx.run(cmd, pty=True)

    @staticmethod
    def psql(ctx, db=''):
        Tasks.ssh(ctx, 'db', executable='psql -U odoo {}'.format(db), quiet=False)

    @staticmethod
    def test(ctx, modules, db='', verbose=False, coverage=False, yes=False, sudo=False, ci=False):
        if modules == 'custom':
            modules = Tasks.details(ctx, 'all', names=True, custom_only=True, pretty=False, prints=False)
            modules = ','.join(modules)
        if not modules:
            shprint(ctx, msg='No modules to test.', color='pink')
            exit(1)

        success = True
        reason = ''
        destroy = False
        version = configs.config.get('options', 'ODOO_VERSION')
        test_method = getattr(Tasks, 'test_{}'.format(version.replace('.', '_')))
        test_results_path = clean_test_dir(ctx, paths.base('.container/testresults'), db)

        if not test_method:
            shprint(ctx, msg='The version {} is not supported for testing.'.format(version), color='pink')
            exit(1)

        # Hack to prevent sharing database containers between ci builds. If they
        # are shared, then there are concurrency issues with odoo training to
        # access the same database containers. It causes concurency errors.
        compose_contents = None
        config_contents = None
        web_container_name = 'web'
        now = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        now = now.lower()

        if ci:
            web_container_name = 'web_{}'.format(now)
            question = ' > WARNING: Are you sure you want to run this (y/n)? It will destroy all containers and networks. This is meant to be run within a ' \
                'continous integration environment. Be very careful with the --ci flag. '

            keep_going = yes or input(shprint(ctx, msg=question, color='lightblue', run=False)) in YES_OPTIONS
            if not keep_going:
                return

            # Stop all active containers first, before we start modifying the
            # configuration files.
            shprint(ctx, msg='Stopping current containers...')
            ctx.run('docker-compose stop')

            with open(paths.base('docker-compose.yml'), 'r') as compose_file:
                compose_contents = compose_file.read()
            with open(paths.base('.container/config/odoo.conf'), 'r') as config_file:
                config_contents = config_file.read()

            shprint(ctx, msg='Assigning new container id {}...'.format(now))
            try:
                ctx.run('sed -i "" "s/^[[:space:]][[:space:]]web:/  web_{}:/" "{}" > /dev/null && '.format(now, paths.base('docker-compose.yml')) +
                        'sed -i "" "s/^[[:space:]][[:space:]]db:/  db_{}:/" "{}" > /dev/null && '.format(now, paths.base('docker-compose.yml')) +
                        'sed -i "" "s/db_host = db/db_host = db_{}/" "{}" > /dev/null && '.format(now, paths.base('.container/config/odoo.conf')) +
                        'sed -i "" "s/-[[:space:]]db$/- db_{}/" "{}" > /dev/null'.format(now, paths.base('docker-compose.yml')))
            except:
                ctx.run('sed -i "s/^[[:space:]][[:space:]]web:/  web_{}:/" "{}" > /dev/null && '.format(now, paths.base('docker-compose.yml')) +
                        'sed -i "s/^[[:space:]][[:space:]]db:/  db_{}:/" "{}" > /dev/null && '.format(now, paths.base('docker-compose.yml')) +
                        'sed -i "s/db_host = db/db_host = db_{}/" "{}" > /dev/null && '.format(now, paths.base('.container/config/odoo.conf')) +
                        'sed -i "s/-[[:space:]]db$/- db_{}/" "{}" > /dev/null'.format(now, paths.base('docker-compose.yml')))

            # Do some more clean up.
            shprint(ctx, msg='Bringing up new containers {}...'.format(now))
            ctx.run('docker-compose build')
            ctx.run('docker-compose up -d db_{}'.format(now))
            ctx.run('sleep 5')  # Make sure postgres has time to initialize

        if not db:
            if yes or input('No database selected. Are you sure you want to create a database to run tests? ').lower() in YES_OPTIONS:
                destroy = True
                db = database.configure_db(ctx, db, modules, verbose=verbose, container=web_container_name)
                shprint(ctx, msg='Created db {}.'.format(db))
                if 'VOLUME_PATH' in os.environ and not os.path.isdir('{}/.container/testresults/{}'.format(os.environ['VOLUME_PATH'], db)):
                    os.mkdir('{}/.container/testresults/{}'.format(os.environ['VOLUME_PATH'], db))
                    shprint(ctx, msg='Created testresults directory.')
            else:
                shprint(ctx, msg='Use the -d flag to select an existing database.')
                exit(0)
        else:
            # TODO, if a database is passed in then we should check if it
            # actually exists, and warn a user if they are about to create a
            # new database from scratch (when they are probably thinking that
            # they are not going to since they used the -d flag)
            pass

        try:
            time.sleep(5)
            test_method(ctx, db, modules, coverage, verbose, sudo=sudo, ci=ci, yes=yes, container=web_container_name)
        except UnexpectedExit as e:
            pass
        except Exception as e:
            pass
        finally:
            # Clean up by destroying any databases, configuration files, or test
            # result files that we no longer need.
            if destroy:
                time.sleep(5)
                database.destroy_db(ctx, db, container='db' if not ci else 'db_{}'.format(now), verbose=verbose)

            has_tests = False
            number_of_tests = 0
            output_path = '{testresults}/{db}/{db}-all.txt'.format(testresults=test_results_path, db=db)

            if ci:
                ctx.run('docker-compose stop')
                ctx.run('docker-compose rm -f')
                if compose_contents:
                    with open(paths.base('docker-compose.yml'), 'w') as compose_file:
                        compose_file.write(compose_contents)
                if config_contents:
                    with open(paths.base('.container/config/odoo.conf'), 'w') as config_file:
                        config_file.write(config_contents)

            if verbose:
                shprint(ctx, msg='Formatting test results...')

            time.sleep(3)
            if os.path.isfile(output_path):
                has_tests = True
                with open(output_path, encoding='utf-8') as output_file:
                    lines = output_file.read().split('\n')
                    for line in lines:
                        line_str = line.replace('"', "'")
                        if u'\u2716' in line_str or 'FAIL' in line_str:
                            success = False
                        if 'odoo.addons' in line_str or 'openerp.addons' in line_str:
                            number_of_tests += 1
                        shprint(ctx, msg=line_str, color=None, encoding='utf-8')

            if not number_of_tests:
                has_tests = False
                success = False
                reason = 'Either no tests exist or no tests could be run.'

            if success:
                if coverage:
                    ctx.run('echo "Running coverage tests..."')
                    ctx.run('docker-compose run {} coverage report --rcfile=/opt/odoo/config/.coveragerc'.format(web_container_name))
            else:
                shprint(ctx, msg='There was a problem running the tests.', color='pink')

            shprint(ctx, msg='----------------------------------------------------------------------', color='lightgrey')
            shprint(ctx, msg=' success?             {}'.format('PASSED' if success else 'FAILED'), color='green' if success else 'pink')
            shprint(ctx, msg=' has tests?           {}'.format('YES' if has_tests else 'NO'), color='green' if has_tests else 'pink')
            shprint(ctx, msg=' number of tests run: {}'.format(number_of_tests), color='lightgrey')
            if reason:
                shprint(ctx, msg=' failure reason:      {}'.format(reason), color='pink')
            shprint(ctx, msg='----------------------------------------------------------------------', color='lightgrey')

            exit(0 if success else 1)

    @staticmethod
    def test_12_0(ctx, db, modules, coverage=False, verbose=False, sudo=False, ci=False, yes=False, container='web'):
        executable = configs.config.get('options', 'ODOO_EXE')
        shprint(ctx, msg='Running the tests on version 12.0...')
        shprint(ctx, msg='    *Testing modules {}...'.format(modules))
        Tasks.run_test(ctx, executable or 'odoo-bin', db, modules, coverage, verbose, extras='-p $(date +%s)', sudo=sudo, ci=ci, yes=yes, container=container)

    @staticmethod
    def test_11_0(ctx, db, modules, coverage=False, verbose=False, sudo=False, ci=False, yes=False, container='web'):
        executable = configs.config.get('options', 'ODOO_EXE')
        shprint(ctx, msg='Running the tests on version 11.0...')
        shprint(ctx, msg='    *Testing modules {}...'.format(modules))
        Tasks.run_test(ctx, executable or 'odoo-bin', db, modules, coverage, verbose, extras='-p $(date +%s)', sudo=sudo, ci=ci, yes=yes, container=container)

    @staticmethod
    def test_10_0(ctx, db, modules, coverage=False, verbose=False, sudo=False, ci=False, yes=False, container='web'):
        executable = configs.config.get('options', 'ODOO_EXE')
        shprint(ctx, msg='Running the tests on version 10.0...')
        shprint(ctx, msg='    *Testing modules {}...'.format(modules))
        Tasks.run_test(ctx, executable or 'odoo-bin', db, modules, coverage, verbose, sudo=sudo, ci=ci, yes=yes, container=container)

    @staticmethod
    def test_9_0(ctx, db, modules, coverage=False, verbose=False, sudo=False, ci=False, yes=False, container='web'):
        executable = configs.config.get('options', 'ODOO_EXE')
        shprint(ctx, msg='Running the tests on version 9.0...')
        shprint(ctx, msg='    *Testing modules {}...'.format(modules))
        Tasks.run_test(ctx, executable or 'openerp-server', db, modules, coverage, verbose, sudo=sudo, ci=ci, yes=yes, container=container)

    @staticmethod
    def run_test(ctx, executable, db, modules, coverage=False, verbose=False, extras='', sudo=False, ci=False, yes=False, container='web'):
        coverage_cmd = 'coverage run --rcfile=/opt/odoo/config/.coveragerc' if coverage else ''
        odoo_executable = ('sudo ' if sudo else '') + '/opt/odoo/core/' + executable
        odoo_flags = "--test-enable --stop-after-init {logging} -d {db} -i {mods} {verbose}".format(
            logging='--logfile=None --log-level=info --log-handler=:INFO' if verbose else '',
            db=db,
            mods=modules,
            verbose='' if verbose else pipe_dev_null)

        run_web_cmd = "docker-compose run {container} {coverage} {exe} {conf} {ports} {flags}".format(
            container=container,
            coverage=coverage_cmd,
            exe=odoo_executable,
            conf="-c /opt/odoo/config/odoo.conf {}".format(extras),
            ports="--xmlrpc-port=7777 --longpolling-port=7788",
            flags=odoo_flags)

        if verbose:
            shprint(ctx, msg='Running the commands:')
            shprint(ctx, msg='    {}'.format(run_web_cmd))
        ctx.run(run_web_cmd, pty=True)

    @staticmethod
    def test_coverage(ctx, modules, db=''):
        test(ctx, modules, db, verbose=False, coverage=True)

    @staticmethod
    def docs(ctx):
        print('Building docs')
        ctx.run('cd {} && make html'.format(paths.base('.docs')))
        ctx.run('cd {} && echo "See docs at http://localhost:8000" && python -m SimpleHTTPServer'.format(
            paths.base('.docs/build/html')), pty=True)

    @staticmethod
    def clean(ctx, rm=False):
        shprint(ctx, msg='Collection cleaned.')

    @staticmethod
    def style(ctx):
        def process_file(filename, filepath):
            cmd = 'cd {} && yapf -i {}'.format(paths.base(), filepath)
            ctx.run(cmd)

        path_helpers.iterate_py_files(process_file, paths.base())

    @staticmethod
    def lint(ctx):
        lint_paths = []

        def process_file(filename, filepath):
            lint_paths.append(filepath)

        path_helpers.iterate_py_files(process_file, paths.base())
        ctx.run('cd {} && pylint {}'.format(paths.base(), ' '.join(lint_paths)))

    @staticmethod
    def new_module(ctx, branch='', name='', verbose=False):
        """
        Create a new module from the module skeleton.

        Essentially this is going to:

          - Clone down our module skeleton repo from bitbucket
          - Prompt the user for some answers about the module
          - Fill out some default (update docs, manifest, index.html, etc.)

        :param ctx {invoke.context.Context}: Invoke context variable
        :param branch {str}:
            The name of the branch to clone, which will typically be the version
            of odoo (9.0, 10.0, 11.0, etc.)
        :param name {str}: The name of the new module
        :param verbose {bool}: True to enable verbose logging/output
        :return {NoneType}:
        """
        ctx.run('echo ""')
        if not name:
            name = input(shprint(ctx, msg=' > What is the technical name of the module? ', color='lightblue', run=False))
        if not branch:
            branch = input(shprint(ctx, msg=' > What is the version of the module (9.0, 10.0, 11.0, etc.)? ', color='lightblue', run=False))

        module_display_name = input(shprint(ctx, msg=' > What is the display name of the module? ', color='lightblue', run=False))
        module_category = input(shprint(ctx, msg=' > What is the category of the module? ', color='lightblue', run=False))
        module_tagline = input(shprint(ctx, msg=' > What is a tagline for the module (1 sentence description)? ', color='lightblue', run=False))
        module_summary = input(shprint(ctx, msg=' > What is a summary/short explanation of the module? ', color='lightblue', run=False))
        ctx.run('echo ""')

        shprint(ctx, msg='Making module...')
        ctx.run('cd {} && git clone https://bitbucket.org/bluestingray/module_scaffold {} --branch="{}" "{}"'.format(
            paths.base(), '--quiet' if not verbose else '', branch, name))
        ctx.run('rm -rf "{}/.git"'.format(paths.base(name)))

        # Wire the defaults to the module. There are a few things that every
        # module needs:
        #
        # 1. New readme.md file
        # 2. Updated __manifest__.py
        # 3. Updated static/description/index.html
        # 4. Updated doc/index.rst
        with open(paths.base('{}/readme.md'.format(name)), 'w') as readme_file:
            readme_file.write('# {} ({})'.format(module_display_name, name))
        with open(paths.base('{}/static/description/index.html'.format(name)), 'w') as index_html_file:
            index_html_file.write('''
<section class="oe_container">
    <div class="oe_row oe_spaced">
        <div class="oe_span12">
            <h2 class="oe_slogan">{}</h2>
            <h3 class="oe_slogan">{}</h3>
        </div>
    </div>
</section>'''.strip('\n').format(module_display_name, module_tagline))
        with open(paths.base('{}/doc/index.rst'.format(name)), 'w') as index_rst_file:
            content = '{} documentation.'.format(name)
            index_rst_file.write('{}\n{}'.format(content, '=' * len(content)))

        manifest_content = False
        manifest_files = ('__manifest__.py', '__openerp__.py')
        for potential_manifest_file in manifest_files:
            if os.path.isfile(paths.base('{}/{}'.format(name, potential_manifest_file))):
                with open(paths.base('{}/{}'.format(name, potential_manifest_file)), 'r') as manifest_file:
                    manifest_content = manifest_file.read()
                    manifest_content = re.sub(r'[\'"]+name[\'"]+:\s+[\'"]+(.*)[\'"]+,', "'name': '{}',".format(module_display_name), manifest_content)
                    manifest_content = re.sub(r'[\'"]+category[\'"]+:\s+[\'"]+(.*)[\'"]+,', "'category': '{}',".format(module_category), manifest_content)
                    manifest_content = re.sub(r'[\'"]+version[\'"]+:\s+[\'"]+(.*)[\'"]+,', "'version': '{}',".format(branch + '.0'), manifest_content)
                    manifest_content = re.sub(r'[\'"]+summary[\'"]+:\s+[\'"]+(.*)[\'"]+,', "'summary': '{}',".format(module_tagline), manifest_content)
                    manifest_content = re.sub(r'[\'"]+description[\'"]+:\s+[\'"]+(.*)[\'"]+,', "'description': '{}',".format(module_summary), manifest_content)
                if manifest_content:
                    with open(paths.base('{}/{}'.format(name, potential_manifest_file)), 'w') as manifest_file:
                        manifest_file.write(manifest_content)

        shprint(ctx, msg='Successfully created the module:')
        shprint(ctx, msg='  name:         {}'.format(name), color='lightgrey')
        shprint(ctx, msg='  branch:       {}'.format(branch), color='lightgrey')
        shprint(ctx, msg='  display name: {}'.format(module_display_name), color='lightgrey')
        shprint(ctx, msg='  category:     {}'.format(module_category), color='lightgrey')
        shprint(ctx, msg='  tagline:      {}'.format(module_tagline), color='lightgrey')
        shprint(ctx, msg='  summary:      {}'.format(module_summary), color='lightgrey')

    @staticmethod
    def image(ctx, project, username, image, tag, push=False):
        ctx.run('docker-compose --project-name {} build'.format(project))
        ctx.run('export DOCKER_ID_USER="{}" && docker login'.format(username), pty=True)
        ctx.run('docker tag odoo_images_web {}/{}:{}'.format(username, image, tag))
        if push:
            ctx.run('docker push {}/{}:{}'.format(username, image, tag))

    @staticmethod
    def details(ctx, module='', names=False, custom_only=False, pretty=False, prints=True):
        if module == 'all':
            modules = Tasks._get_modules(module, custom_only)
            if not modules:
                shprint(ctx, msg='Could not find modules with that information.', color='pink')

            # Only care about generating a list of names for the modules in this
            # project.
            if names:
                separator = '\n' if pretty else ','
                if prints:
                    shprint(ctx, msg=separator.join(modules), color='green' if pretty else None)
                return modules

            # Otherwise we are generate full details on the modules.
            else:
                shprint(ctx, msg='Coming soon...')
        shprint(ctx, msg='Coming soon...')

    @staticmethod
    def _get_modules(module, custom_only=False):
        if module == 'all':
            if custom_only:
                module_directories = []

                directory_names = list(filter(lambda dirname: dirname and os.path.isdir(dirname) and dirname[0] not in ['_', '.'], os.listdir()))
                for directory_name in directory_names:
                    if os.path.isfile('{}/__manifest__.py'.format(directory_name)) or os.path.isfile('{}/__openerp__.py'.format(directory_name)):
                        module_directories.append(directory_name)

                if os.path.isdir('_lib'):
                    lib_directory_names = list(filter(lambda dirname: dirname and os.path.isdir('_lib/' + dirname), os.listdir('_lib')))
                    for directory_name in lib_directory_names:
                        manifest_path = '_lib/{}/__manifest__.py'.format(directory_name)
                        openerp_path = '_lib/{}/__openerp__.py'.format(directory_name)
                        if os.path.isfile(manifest_path) or os.path.isfile(openerp_path):
                            module_directories.append(directory_name)

                if os.path.isdir('_lib_static'):
                    lib_static_directory_names = list(filter(lambda dirname: dirname and os.path.isdir('_lib_static/' + dirname), os.listdir('_lib_static')))
                    for directory_name in lib_static_directory_names:
                        manifest_path = '_lib_static/{}/__manifest__.py'.format(directory_name)
                        openerp_path = '_lib_static/{}/__openerp__.py'.format(directory_name)
                        if os.path.isfile(manifest_path) or os.path.isfile(openerp_path):
                            module_directories.append(directory_name)

                return module_directories
            else:
                return []
        return []

    @staticmethod
    def deploy(ctx):
        shprint(ctx, msg='Deploying...')

    @staticmethod
    def mkdocs(ctx, template_dir):
        if not os.path.isdir(template_dir):
            error = "Error: %s does not exist or is not a directory." % (template_dir)
            shprint(ctx, msg=error, color='pink')
            return None
        templates = _mkdoc_get_templates(template_dir)
        for template in templates:
            context = _mkdoc_get_context(template, template_dir)
            output_file = template[:-5] + "/static/description/index.html"
            with open(output_file, "w") as doc:
                print(_mkdoc_render(template_dir + template, context), file=doc)
