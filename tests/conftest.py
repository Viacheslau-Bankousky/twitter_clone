"""
This module sets up basic Fixtures for the pytest to use during testing.

The fixtures handle setting up and tearing down the testing database tables.

Modules:
--------
- pytest to provide fixtures
- httpx to create an AsyncClient object for client simulation
- ASGITransport from httpx to transport requests for the AsyncClient
    object
- Base from application.models.base_model to interact with database schema
- test_engine from application.database.connection for setting up and tearing
    down the database

"""
from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from application.database.connection import test_engine
from application.models.base_model import Base
from tests.app_for_testing.application import test_app
from tests.helpers.values import BASE_URL


@pytest_asyncio.fixture(scope="function", autouse=True)
async def set_up_testing_database() -> AsyncGenerator:
    """
    Use to set up the testing database before each test.

    Done by creating all tables in the Base metadata using the test_engine.

    Yields:
        None.
        After setting up, surrenders control back to the test execution.
        Automatically used due to 'autouse=True'.
    """
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture(scope="function")
async def take_async_client() -> AsyncGenerator:
    """
    Yield an AsyncClient object that tests can use to make requests.

    Yields:
        An instance of AsyncClient.
    """
    async with AsyncClient(
        base_url=BASE_URL,
        transport=ASGITransport(app=test_app),  # type: ignore
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture(scope="function", autouse=True)
async def teardown_testing_database() -> AsyncGenerator:
    """
    Use to clean up the testing database after each test.

    Done by dropping all tables in the Base metadata using the test_engine.

    Yields:
        None.
        After the tear-down is complete, surrenders control back to the test
        execution.
        Automatically used due to 'autouse=True'.
    """
    yield
    async with test_engine.begin() as cleanup_connection:
        await cleanup_connection.run_sync(Base.metadata.drop_all)
