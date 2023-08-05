from invoke import task
from subprocess import check_output
from .lib.shell import shprint


@task
def docs(ctx, files=None, staged=False):
    """
    Automatically format all docstrings in the provided (or staged) files.

    This is done with the `docformatter` package using its built-in options.
      - https://pypi.org/project/docformatter/

    Note: It's likely that docformatter can be extended to handle some of the
          more unique docstring formats that we want to enforce, such as
          parameter formatting.

    Example uses:
        - invoke format.docs -f module/path/to/file.py,module2/path/to/file2.py
        - invoke format.docs --staged

    :param files {str}: comma-separated string of file names with relative paths
    :param staged {bool}:
        (optional) if True, docs formatting will be run on all staged files,
        including any unstaged parts of the staged files.
    :return {NoneType}:
    """
    if files and staged:
        shprint(ctx, msg='You should provide --files or --staged, but not both')
        exit(1)
    if files:
        # Convert comma-separated string into space-separated string
        files = files.replace(',', ' ')
    if staged:
        # Get names of staged files from git and replace newlines with spaces
        files = check_output(['git', 'diff', '--name-only', '--cached']).decode('utf-8').replace('\n', ' ')

    ctx.run("docformatter -i --wrap-summaries 80 --wrap-descriptions 80 --pre-summary-newline --make-summary-multi-line {}".format(files))
