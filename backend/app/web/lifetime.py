from typing import Awaitable, Callable

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.db import engine


def _setup_db(app: FastAPI) -> None:
    """
    Creates connection to the database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application.
    """

    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    app.state.db_engine = engine  # noqa
    app.state.db_session_factory = session_factory  # noqa


def register_startup_event(
        app: FastAPI,
) -> Callable[[], Awaitable[None]]:
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:
        app.middleware_stack = None
        _setup_db(app)
        app.middleware_stack = app.build_middleware_stack()
        pass

    return _startup


def register_shutdown_event(
        app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        await app.state.db_engine.dispose()  # noqa
        pass

    return _shutdown
