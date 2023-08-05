import getpass
import json
import requests

from invoke import task
from .lib.tasks import Tasks


@task
def authenticate(ctx, url, db, user, verbose=False):
    """
    Authenticate with an instance via curl.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param url:
    :param db:
    :param user:
    :return:
    """
    Tasks.setup(ctx)
    password = getpass.getpass('Odoo User Password? ')
    data = {'params': {'db': db,
                       'login': user,
                       'password': password, }, }

    cmd = "curl -X POST -H 'Content-type: application/json' {url}/web/session/authenticate -d '{jsondata}'"
    result = ctx.run(cmd.format(url=url, jsondata=json.dumps(data)), hide=True)
    response = json.loads(result.stdout)
    sessionid = response['result']['session_id']

    if verbose:
        ctx.run("echo {} | json_pp".format(json.dumps(result.stdout)))
    ctx.run('echo "Authenticated, session={}"'.format(sessionid))

    return sessionid, response


@task
def json(ctx, url, method, session='', db='', user='', verbose=False):
    """
    Curl JSON data to an endpoint. Used to interact with/test odoo controllers
    and routes.

    :param ctx {invoke.context.Context}: Invoke context variable
    :param url:
    :param method:
    :param session:
    :param db:
    :param user:
    :param verbose:
    :return {NoneType}:
    """
    Tasks.setup(ctx)

    if session:
        sessionid = session
    else:
        sessionid, _ = curl_authenticate(ctx, url, db, user, verbose=verbose)

    cmd = "curl -X {method} -H 'Content-type: application/json' --cookie 'session_id={sessionid}' -d '{data}' {url}"
    result = ctx.run(cmd.format(method=method, sessionid=sessionid, data='{}', url=url), hide=True)
    ctx.run("echo {} | json_pp".format(json.dumps(result.stdout)))
