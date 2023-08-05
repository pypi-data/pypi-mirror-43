import os
import sys
import filecmp
import jinja2
import json
import shutil
import getpass
import requests
from urllib.parse import quote

from . import configs
from .shell import shprint
from . import paths as path_helpers

pipe_dev_null = path_helpers.pipe_dev_null
paths = path_helpers.Paths()


def snippet(path, data, out=None):
    if not os.path.isfile(path):
        raise Exception('File {} does not exist...'.format(path))

    contents = None
    dot_data = _dict_to_dot_syntax(data)
    with open(path) as snippet_template:
        contents = snippet_template.read()
        for key in dot_data:
            identifier = '{{' + key + '}}'
            if identifier in contents:
                contents = contents.replace(identifier, str(dot_data[key]))

    if out:
        with open(out, 'w+') as out_file:
            out_file.write(contents)

    return contents


def _dict_to_dot_syntax(data, res=None, parent=None):
    res = res or {}
    parent = parent or []

    for key in data:
        parent.append(key)
        if isinstance(data[key], dict):
            res = _dict_to_dot_syntax(data[key], res, parent)
            parent.pop()
        else:
            res['.'.join(parent)] = data[key]
            parent.pop()

    return res


def _mkdoc_render(template, context):
    """
    Given a template path and a context variable, return the rendered template
    as a string of HTML.

    :param template {str}:
    :param context {list}:
    :return {jinja2.Environment}:
    """
    path, filename = os.path.split(template)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)


def _mkdoc_get_templates(path):
    """
    Gets a list of templates to render. The template must have the same name
    as the module. This will skip base.html.

    :param path {str}:
    :return {list}:
    """
    templates = []
    for item in [filename for filename in os.listdir(path) if filename[-5:] == '.html']:
        templates.append(item)
    templates.remove('base.html')
    return templates


def _mkdoc_get_context(template_name, template_path):
    """
    :param template_name {str}:
    :param template_path {str}:
    :return {list}:
    """
    jsonfile = template_path + "vars/" + template_name[:-5] + ".json"
    with open(jsonfile) as j:
        context = json.load(j)
    return context


def _check(params, errors):
    """
    Check if all of the parameters exist or not, and print the corresponding
    error if one is not passed through.

    :param params:
    :param errors:
    :return {NoneType}:
    """
    for index, param in enumerate(params):
        if not param:
            print(errors[index])
            exit(0)


def _iterate_py_files(fn):
    """
    :param fn:
    :return {NoneType}:
    """
    ignore = ['.container', '.deployment', '.docs', '.githooks',
              '.monitoring', '.om', '_lib', '_lib_static']
    for dirpath, dirs, filenames in os.walk(paths.base(), topdown=True):
        dirs[:] = [d for d in dirs if d not in ignore]
        for filename in [f for f in filenames if f.endswith(".py") and f not in ignore]:
            fn(filename, os.path.join(dirpath, filename))


def _iterate_odoo_modules(fn):
    """
    :param fn:
    :return {NoneType}:
    """
    pass


def _toggl_modules(ctx):
    """
    :param ctx {invoke.context.Context}: Invoke context variable
    :return {NoneType}:
    """
    pass


def _enable_module(ctx, module):
    """
    :param ctx {invoke.context.Context}: Invoke context variable
    :param module:
    :return {NoneType}:
    """
    pass


def _disable_module(ctx, module):
    """
    :param ctx {invoke.context.Context}: Invoke context variable
    :param module:
    :return {NoneType}:
    """
    pass


def _get_container_id_cmd(ctx, container):
    """
    :param ctx {invoke.context.Context}: Invoke context variable
    :param container {str}:
    :return {str}:
    """
    get_container_id_cmd = 'docker ps -q --filter "name={}_{}"'.format(os.path.basename(os.path.dirname(paths.base('.om'))), container)
    # We are running this and ignoring the output only because this
    # command will error out if we cannot find the container that someone
    # is trying to ssh into. If no error, then we'll just continue.
    ctx.run(get_container_id_cmd + ' > /dev/null')
    return "export containerid=$({})".format(get_container_id_cmd)


def _get_container_exec_cmd(ctx, container, flags, command):
    """
    This is a helper so that you can run the `docker exec` command on a specific
    container. This method will handle getting the container id for you
    automatically.

    A call to the function like this:

    ```
    _get_container_exec_cmd('web', '-it', '/bin/bash')
    ```

    Would result in an output of:

    ```
    export containerid=ijo12b3iou1123 && docker exec -it $containerid /bin/bash
    ```

    where ijo12b3iou1123 is the id of the web container

    :param container {str}:
    :param flags {str}:
    :param command {str}:
    :return {str}:
    """
    container_cmd = _get_container_id_cmd(ctx, container)
    shell_cmd = "docker exec {} $containerid {}".format(flags, command)
    return container_cmd, shell_cmd, "{} && {}".format(container_cmd, shell_cmd)


def _get_container_sh_cmd(ctx, container, command):
    """
    This command is identical to the _get_container_exec_cmd command except we
    are going to run a standard shell command instead of specifically running
    the docker exec command.

    A call to the function like this:

    ```
    _get_container_sh_cmd('db', 'docker restart $containerid')
    ```

    Would result in an output of:

    ```
    export containerid=aoijaowdoiajwd && docker restart $containerid
    ```

    where aoijaowdoiajwd is the id of the db container

    :param container {str}:
    :param command {str}:
    :return {str}:
    """
    if '$containerid' not in command:
        raise Exception(
            'Make sure that you reference `$containerid` somewhere in your command argument.')

    container_cmd = _get_container_id_cmd(ctx, container)
    return "{} && {}".format(container_cmd, command)


MANIFEST = '__manifest__.py'
LEGACY_MANIFEST = ['__addons_manifest__.py']


class console_colors(object):
    """
    Helper to hold some constant for shell colors.
    """

    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


def parse_config():
    """
    Read and parse out the __addons_manifest.py config that sits in the root
    directory of module collection folders.

    This will throw an exception and exit the CLI program / make program all
    together if the file cannot be read properly or the file cannot be parsed
    (exec) properly.

    :raises Exception:
    :return {dict}:
    """
    try:
        f = open(paths.base(MANIFEST), 'r').read()
        return eval(f)
    except Exception as e:
        for legacy_format in LEGACY_MANIFEST:
            if os.path.isfile(paths.base(legacy_format)):
                shutil.move(paths.base(legacy_format), paths.base(MANIFEST))
                try:
                    f = open(paths.base(MANIFEST), 'r').read()
                    return eval(f)
                except Exception as e:
                    continue
        print('There was a problem processing your __manifest__.py file for the project. Make sure it exists and is in a valid format.' + "\n")
        exit(1)


def print_diff_files(ctx, dcmp):
    """
    :param ctx {invoke.context.Context}: Invoke context variable
    :param dcmp:
    :return {NoneType}:
    """
    for name in dcmp.diff_files:
        print(console_colors.WARNING + "diff_file {} found in {} and {}".format(name,
                                                                                dcmp.left, dcmp.right) + console_colors.ENDC)
    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(ctx, sub_dcmp)


def _git_clone(ctx, url, branch, output, depth=1):
    """
    Does a system call on git clone, returns the exit status from that system.

    :param url {str}:
    :param branch {str}:
    :return {int}: Returns int representing success or failure
    """
    return ctx.run('git clone {url} {output} --branch={branch} --depth={depth} --quiet{pipe}'.format(url=url,
                                                                                                     branch=branch,
                                                                                                     output=output,
                                                                                                     depth=depth,
                                                                                                     pipe=redirect()))


def _get_git_config():
    git_config = {}
    # right now, just assuming bitbucket.org repo's
    if not configs.config.has_option('options', 'USERNAME') or not configs.config.has_option('options', 'PASSWORD'):
        git_config['username'] = quote(input("bitbucket username? "))
        git_config['password'] = quote(getpass.getpass("bitbucket password? "))
    else:
        git_config['username'] = configs.config.get('options', 'USERNAME')
        git_config['password'] = configs.config.get('options', 'PASSWORD')
    return git_config


def _get_git_urls(repo_url):
    if repo_url[:4] == 'http':
        http_url = repo_url
        ssh_url = repo_url.replace('https://', 'git@')\
            .replace('http://', 'git@')\
            .replace('.com/', '.com:')\
            .replace('.org/', '.org:')
    else:
        ssh_url = repo_url
        http_url = repo_url.replace('git@', 'https://')\
            .replace('.com:', '.com/')\
            .replace('.org:', '.org/')

    return {'ssh': ssh_url, 'http': http_url}


def git_clone(ctx, url, branch, repo_name, output, depth=1):
    urls = _get_git_urls(url)
    try:
        shprint(ctx, msg='        *Trying to clone {}...'.format(urls['ssh']), color='yellow')
        _git_clone(ctx, urls['ssh'], branch, output, depth=depth)
    except:
        try:
            shprint(ctx, msg='        *Trying to clone {}...'.format(urls['http']), color='yellow')
            _git_clone(ctx, urls['http'], branch, output, depth=depth)
        except:
            try:
                credentials = _get_git_config()
                credentials_url = 'https://{username}:{password}@{url}'.format(
                    username=credentials.get('username'),
                    password=credentials.get('password'),
                    url=urls['http'][8:])
                shprint(ctx, msg='        *Trying to clone {}...'.format(credentials_url), color='yellow')
                _git_clone(ctx, credentials_url, branch, output, depth=depth)
            except:
                shprint(ctx, msg='        Sorry, could not clone the repo {}'.format(repo_name), color='red')


def diff_dependency_git(ctx, name, module_config, log=True):
    """
    :param name:
    :param module_config:
    :return: dict Paths for the modules
    """
    if log:
        shprint(ctx, msg='  Processing {}...'.format(name), color='yellow')

    repo_name = module_config['url'].replace('.git', '').split('/').pop()
    repo_temp_path = paths.base('_make_tmp/{}'.format(repo_name))
    original_path = paths.base('_lib/{}'.format(name))

    # If there is no repo cloned down into the temp folder yet, then we are going to git clone it
    # down so that we can access modules that we need to move into _lib.
    if not os.path.isdir(repo_temp_path):
        shprint(ctx, msg='    *Starting git clone for {}...'.format(module_config['url']), color='yellow')

        repo_url = module_config['url']
        repo_branch = module_config['branch']
        git_clone(ctx, repo_url, repo_branch, repo_name, output=paths.base('_make_tmp/{}'.format(repo_name)))

    # Once we've got the modules and files setup, then we are going to check and see if we want
    # to run a diff on these these or not.
    if os.path.isdir(paths.base('{temp_path}/{module_name}'.format(temp_path=repo_temp_path, module_name=name))):
        temp_module_path = paths.base('{temp_path}/{module_name}'.format(temp_path=repo_temp_path, module_name=name))
        if log and os.path.isdir(original_path):
            print_diff_files(ctx, filecmp.dircmp(original_path, temp_module_path))
    else:
        shprint(ctx, msg=' ** Unable to find {module_name} in {repo}.'.format(repo=module_config['url'], module_name=name), color='red')
        exit(1)

    return {'original': original_path, 'updated': temp_module_path}


def diff_dependency(ctx, name, module_config, log=True):
    """
    :param ctx {invoke.context.Context}: Invoke context variable
    :param name {str}:
    :param module_config:
    :return {NoneType}:
    """
    if 'type' in module_config:
        fn = getattr(sys.modules[__name__], 'diff_dependency_{type}'.format(
            type=module_config['type']))
        if fn:
            return fn(ctx, name, module_config, log)
    else:
        return diff_dependency_git(ctx, name, module_config, log)


def update_dependency(ctx, name, module_config):
    """
    :param ctx {invoke.context.Context}: Invoke context variable
    :param name {str}:
    :param module_config:
    :return {NoneType}:
    """
    diff_paths = diff_dependency(ctx, name, module_config, log=False)
    shprint(ctx, msg="  Updating lib with {}...".format(os.path.basename(diff_paths['original'])), color='yellow')
    os.system('rm -rf {}'.format(diff_paths['original']))
    os.system('cp -R {} {}'.format(diff_paths['updated'], diff_paths['original']))


def cleanup():
    """
    Cleans up everything related to the make process that runs for this specific
    module collection.

    :return {NoneType}:
    """
    os.system('rm -rf {}'.format('_make_tmp'))


def clean_test_dir(ctx, test_results_path, db):
    """
    :param ctx {invoke.context.Context}: Invoke context variable
    :param test_results_path:
    :param db:
    :return {NoneType}:
    """

    if not os.path.isdir(test_results_path):
        test_results_path = '../{}'.format(test_results_path)
        if not os.path.isdir(test_results_path):
            ctx.run('mkdir -p {}'.format(test_results_path))

    # Clean up the existing test results folder before we move on to actually
    # creating databases and running tests.
    test_results_db_path = '{testresults}/{db}'.format(
        testresults=test_results_path, db=db)
    if os.path.isdir(test_results_db_path):
        shutil.rmtree(test_results_db_path)

    return test_results_path


def redirect(verbose=False):
    """
    :param verbose {bool}:
    :return {str}:
    """
    return '' if verbose else (' ' + pipe_dev_null)


def env():
    """
    :return {str}:
    """
    if configs.config.has_option('options', 'ENVIRONMENT'):
        return configs.config.get('options', 'ENVIRONMENT')
    return 'development'
