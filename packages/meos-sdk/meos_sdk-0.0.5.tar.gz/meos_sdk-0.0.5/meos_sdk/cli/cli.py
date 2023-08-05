import os
import sys
import traceback

from flask import Flask
from meos_sdk.app import MeosApp

import click


class NoAppException(click.UsageError):
    """Raised if an application cannot be found or loaded."""


def prepare_import(path):
    """Given a filename this will try to calculate the python path, add it
    to the search path and return the actual module name that is expected.
    """
    path = os.path.realpath(path)

    fname, ext = os.path.splitext(path)
    if ext == '.py':
        path = fname

    if os.path.basename(path) == '__init__':
        path = os.path.dirname(path)

    module_name = []

    # move up until outside package structure (no __init__.py)
    while True:
        path, name = os.path.split(path)
        module_name.append(name)

        if not os.path.exists(os.path.join(path, '__init__.py')):
            break

    if sys.path[0] != path:
        sys.path.insert(0, path)

    return '.'.join(module_name[::-1])


def locate_app(*, module_name: str) -> Flask:
    try:
        __import__(module_name)
    except ImportError:
        # Reraise the ImportError if it occurred within the imported module.
        # Determine this by checking whether the trace has a depth > 1.
        if sys.exc_info()[-1].tb_next:  # type: ignore
            raise NoAppException(
                'While importing "{name}", an ImportError was raised:'
                '\n\n{tb}'.format(name=module_name, tb=traceback.format_exc())
            )
        else:
            raise NoAppException(
                'Could not import "{name}".'.format(name=module_name)
            )

    module = sys.modules[module_name]
    for value in module.__dict__.values():
        if isinstance(value, MeosApp):
            app: MeosApp = value
    return app


@click.group()
@click.pass_context
def meos_sdk(ctx):
    pass


@meos_sdk.command()
@click.option('--app', '-a', default='app.app.app',
              help='The import path to your MeosApp object')
@click.option('--host', '-h', default='127.0.0.1',
              help='The interface to bind to.')
@click.option('--port', '-p', default=5000,
              help='The port to bind to.')
@click.option('--debug', default=1,
              help='Set if debug mode'
              'is active if debug is enabled.')
def run(app: str, host, port, debug):
    import_name = prepare_import(app)
    _debug = bool(debug)
    _app = locate_app(module_name=import_name)
    if _debug:
        _app.run(host=host, port=port, debug=_debug)
    else:
        app_object_name = app.split('.')[-1]
        os.system(
            f'PYTHONPATH=. uwsgi --http {host}:{port} --module {app} '
            f'--callable {app_object_name} '
            '--processes 4 --harakiri 30 '
            '--enable-threads --single-interpreter '
            '--master --thunder-lock --http-keepalive '
            '--ignore-sigpipe --ignore-write-errors '
            '--disable-write-exception'
        )
