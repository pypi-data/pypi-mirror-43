import os
import re

U_SUCCESS = u'\u2713'
U_FAILURE = u'\u2716'


def shprint(ctx, msg, color='green', run=True, **kwargs):
    """
    Run an echo command through invoke that prints text in color.

    We will be using the following color codes:

    Black        0;30     Dark Gray     1;30
    Red          0;31     Light Red     1;31
    Green        0;32     Light Green   1;32
    Brown/Orange 0;33     Yellow        1;33
    Blue         0;34     Light Blue    1;34
    Purple       0;35     Light Purple  1;35
    Cyan         0;36     Light Cyan    1;36
    Light Gray   0;37     White         1;37

    :param ctx {invoke.context.Context}: Invoke context variable
    :param msg {str}:
    :param color {str}:
    :param run {bool}:
    :return {NoneType}:
    """
    if os.environ.get('INVOKE_ASCII', False) == '1':
        msg = msg.replace(U_SUCCESS, 'PASS')
        msg = msg.replace(U_FAILURE, 'FAIL')
        msg = msg.encode('utf-8').decode('ascii', 'ignore')

    if run and os.environ.get('INVOKE_NO_COLOR', False) == '1':
        msg = re.sub(r'\s*\$\(tput[a-z0-9 ]+\)\s*', '', msg)
        ctx.run('echo "{}"'.format(msg), **kwargs)
        return msg

    reset = '\033[0m'
    colors = {'red': '\033[0;31m',
              'green': '\033[0;32m',
              'yellow': '\033[0;33m',
              'blue': '\033[0;34m',
              'purple': '\033[0;35m',
              'lightblue': '\033[1;34m',
              'lightgrey': '\033[0;37m',
              'grey': '\033[1;30m',
              'pink': '\033[1;31m', }

    color = '' if (not color or color not in colors) else colors[color]
    msg = '{}{}{}'.format(color, msg, reset)
    if run:
        ctx.run('echo "{}"'.format(msg), **kwargs)
    return msg
