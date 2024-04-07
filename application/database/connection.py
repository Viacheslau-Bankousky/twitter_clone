"""
This module sets up connections to production and testing databases.

It exports an async context manager `get_session` for establishing
database sessions.

It uses async SQLAlchemy to connect to the PostgreSQL database for
production runtime, and an SQLite database in memory for testing.
These sessions are committed after successful execution of tasks,
and rolled back in the case of any exceptions.

A dotenv mechanism is provided to load environment variables
(DB_USER, DB_PASSWORD)

Modules:
--------
os: Fetching environment variables
contextlib: Context manager utilities
typing: Type annotations
dotenv: Load environment variables from .env into the environment
sqlalchemy.ext.asyncio: SQLAlchemy's asyncio support that provides
asyncio-compatible Engine and Session classes
application.logger.logger_instance: Application level logger instance

Functions:
----------
get_session(testing=False) -> AsyncGenerator[AsyncSession, None]:
    A async Context manager that manages database sessions for you.
"""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable, Optional

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from application.logger.logger_instance import app_logger

load_dotenv()

DB_USER: Optional[str] = os.getenv("DB_USER")
DB_PASSWORD: Optional[str] = os.getenv("DB_PASSWORD")
DB_URL: str = "postgresql+asyncpg://{0}:{1}@db:5432/twitter_clone_db".format(
    DB_USER,
    DB_PASSWORD,
)
TESTING_DB_URL: str = "sqlite+aiosqlite:///:memory:"
engine: AsyncEngine = create_async_engine(
    DB_URL,
    echo=True,
    poolclass=NullPool,
)
test_engine: AsyncEngine = create_async_engine(
    TESTING_DB_URL,
    connect_args={"check_same_thread": False},
)
TestingAsyncSession: Callable[..., AsyncSession] = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)
ProductionAsyncSession: Callable[..., AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


@asynccontextmanager
async def get_session(testing=None) -> AsyncGenerator[AsyncSession, None]:
    """
    Asynchronous context manager that generates a database session.

    This function establishes a session to the database which could be either
    testing or production based on the provided value for the `testing`
    parameter.
    It commits the changes and closes the session automatically once session
    operations are completed. In the event of an exception, it rolls back the
    session and re-raises the exception.

    Args:
        testing (bool, optional): A flag that indicates the type of session.
            `True` creates a testing database session.
            `False` or `None` creates a production database session.
            By default `None`, at which point the value is retrieved from the
            environment variable 'TESTING'.

    Yields:
        AsyncSession: The active database session.

    Raises:
        Exception: Any exception that occurred while performing session
            operations is propagated.

    """
    app_logger.info("Establishing database session")
    if testing is None:
        testing = os.getenv('TESTING') == 'true'
    session = (
        TestingAsyncSession() if testing is True else ProductionAsyncSession()
    )

    try:  # noqa: WPS229
        yield session
        await session.commit()
        app_logger.info("Database session commit successful")
    except Exception as ex:
        app_logger.exception("An error occurred with the database session")
        await session.rollback()
        raise ex
    finally:
        await session.close()
        app_logger.info("Database session closed")
