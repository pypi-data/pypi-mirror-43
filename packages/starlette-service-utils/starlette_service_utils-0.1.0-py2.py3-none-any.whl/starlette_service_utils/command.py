import asyncio
import functools
import importlib
import inspect
import operator
import typing

import click
import IPython
import uvicorn
import starlette.applications
import starlette.testclient

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.4.4"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"
__all__ = ['common_cli', 'CommandEnv', 'starlette_triggers']


class CommandEnv:

    app: starlette.applications.Starlette
    app_name: str
    shell_imports: typing.List[typing.Tuple[str, str]] = []
    shell_producers: typing.List[typing.Callable[[starlette.applications.Starlette], typing.Dict[str, typing.Any]]] = []
    shell_cleanups: typing.List[typing.Callable[[typing.Dict], None]] = []
    default_port: str = '8080'
    default_host: str = '127.0.0.1'

    @classmethod
    def run_cli(cls):
        sources = [common_cli]
        try:
            command_module = importlib.import_module(cls.app_name + '.commands')
            sources.extend(
                map(
                    operator.itemgetter(1),
                    inspect.getmembers(command_module, lambda x: isinstance(x, click.Group))
                )
            )
        except ModuleNotFoundError:
            pass
        click.CommandCollection(sources=sources)()


def starlette_triggers(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with starlette.testclient.TestClient(CommandEnv.app):
            result = func(*args, **kwargs)
        return result

    return wrapper


def async_command(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))
    return wrapper


@click.group()
def common_cli():
    pass


@common_cli.command()
@click.option('--host', default=lambda: CommandEnv.default_host)
@click.option('--port', default=lambda: CommandEnv.default_port, type=int)
@click.option('--workers', default=1, type=int)
@click.option('--debug/--no-debug', default=False)
@click.option('--auto-reload/--no-auto-reload', default=False)
def run(host, port, workers, debug, auto_reload):
    uvicorn.run(
        CommandEnv.app,
        host=host,
        port=port,
        debug=debug,
        loop='uvloop',
        reload=auto_reload,
        workers=workers
    )


@common_cli.command()
@starlette_triggers
def shell():
    user_ns = {}
    for module, elements in CommandEnv.shell_imports:
        module = importlib.import_module(module)
        if elements == '*':
            if hasattr(module, '__all__'):
                for element_name in module.__all__:
                    user_ns[element_name] = getattr(module, element_name)
            else:
                user_ns.update({
                    x[0]: x[1] for x in
                    inspect.getmembers(module, lambda x: not inspect.ismodule(x))
                    if not (x[0].startswith('__') and x[0].endswith('__'))
                })
    for shell_producer in CommandEnv.shell_producers:
        user_ns.update(shell_producer(CommandEnv.app))
    IPython.embed(
        header=f'Welcome to {CommandEnv.app_name} shell',
        autoawait=True,
        loop_runner='asyncio',
        user_ns=user_ns
    )
    for shell_cleanup in CommandEnv.shell_cleanups:
        shell_cleanup(user_ns)
    print('Good luck!')
