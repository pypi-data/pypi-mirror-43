import asyncio
import functools

import starlette.applications
import starlette.config


__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.1.2"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

__all__ = [
    'config', 'sentry_integration', 'aiohttp_integration',
    'anji_orm_integration', 'run_background_task', 'background_tasks_integration'
]

config = starlette.config.Config('.env')
BACKGROND_TASK_LIST = []


def async_partial(func, *partial_args, **partial_kwargs):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        kwargs.update(partial_kwargs)
        return await func(*partial_args, *args, **kwargs)
    return wrapper


async def init_sentry_integration(starlette_app: starlette.applications.Starlette) -> None:
    import sentry_sdk
    import sentry_asgi

    if config('SENTRY_DSN', default=None):
        sentry_sdk.init(
            dsn=config('SENTRY_DSN', default=None),
            release=config('VERSION', default='local'),
            environment=config('ENVIRONMENT', default='dev'),
            integrations=[]
        )
        starlette_app.add_middleware(sentry_asgi.SentryMiddleware)


def sentry_integration(starlette_app: starlette.applications.Starlette) -> None:
    starlette_app.add_event_handler('startup', async_partial(init_sentry_integration, starlette_app))


async def init_aiohttp_session(sanic_app, _loop) -> None:
    import aiohttp

    session_kwargs = {}
    if not sanic_app.config.get('VERIFY_SSL', True):
        session_kwargs['connector'] = aiohttp.TCPConnector(verify_ssl=False)
    sanic_app.async_session = aiohttp.ClientSession(**session_kwargs)  # type: ignore


async def close_aiohttp_session(sanic_app, _loop) -> None:
    await sanic_app.async_session.close()


def aiohttp_integration(starlette_app: starlette.applications.Starlette) -> None:
    starlette_app.add_event_handler('startup', async_partial(init_aiohttp_session, starlette_app))
    starlette_app.add_event_handler('shutdown', async_partial(close_aiohttp_session, starlette_app))


async def initial_anji_orm_configuration() -> None:
    from anji_orm import orm_register

    extensions = {}
    if config('ANJI_ORM_FILE_EXTENSION_CONNECTION_STRING', default=None):
        extensions['file'] = config('ANJI_ORM_FILE_EXTENSION_CONNECTION_STRING', default=None)

    orm_register.init(
        config('ANJI_ORM_CONNECTION_STRING', default='rethinkdb://'),
        {},
        async_mode=True,
        extensions=extensions
    )
    await orm_register.async_load()


async def stop_anji_orm() -> None:
    from anji_orm import orm_register

    await orm_register.async_close()


def anji_orm_integration(starlette_app: starlette.applications.Starlette) -> None:
    starlette_app.add_event_handler('startup', initial_anji_orm_configuration)
    starlette_app.add_event_handler('shutdown', stop_anji_orm)


def run_background_task(coroutine) -> None:
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    task = loop.create_task(coroutine)
    BACKGROND_TASK_LIST.append(task)


async def stop_background_tasks() -> None:
    for task in BACKGROND_TASK_LIST:
        task.cancel()

    await asyncio.wait(BACKGROND_TASK_LIST)


def background_tasks_integration(starlette_app: starlette.applications.Starlette) -> None:
    starlette_app.add_event_handler('shutdown', stop_background_tasks)
