import os
from invoke import task
from .lib.shell import shprint


@task
def search(ctx, search_param):
    """
    Open the default browser to the Blue Stingray ERP Wiki with the results for
    the provided search term.

    :param search_param {str}:
        Search parameter(s) to search. Use + instead of spaces to separate
        search terms, such as: "something+cool"
    :return {NoneType}:
    """
    open_command = False
    wiki_search_url = 'https://wiki.bluestingray.com/doku.php?do=search&id=teams%3Aerp%3Astyle-guide&q='

    os_type = str(os.uname()).lower()
    if 'linux' in os_type :
        open_command = 'xdg-open'
    else:
        open_command = 'open'

    if not open_command:
        shprint(ctx, msg='What OS are you on?')
    else:
        ctx.run('{} "{}{}"'.format(open_command, wiki_search_url, search_param))
