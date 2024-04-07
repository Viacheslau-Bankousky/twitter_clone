"""
This module includes fixtures for adding new users.

The main purpose of this module is to provide an automated setup for
adding new users.

Modules:
--------
- `pytest_asyncio` to use asynchronous fixtures for testing asyncio
    Python code.
- `tests.helpers.values` for reference values like ADD_USER_ROUTE
    and TIMEOUT.
"""
import pytest_asyncio

from tests.helpers.values import ADD_USER_ROUTE, TIMEOUT


@pytest_asyncio.fixture(scope="function", autouse=True)
async def add_new_users(take_async_client) -> None:
    """
    Add new users using HTTP POST method.

    This fixture uses an async HTTP client to POST JSON data, which represents
    new users, to a specific URL.
    Two users, "Bob" and "Pit", are added with their corresponding API keys,
    "test" and "second-test" respectively.
    The URL and timeout value for the request are retrieved from the
    `tests.helpers.values` module.

    The fixture is set to run automatically for each function where it's used
    due to the `autouse` parameter being set to True.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.

    """
    await take_async_client.post(
        url=ADD_USER_ROUTE,
        timeout=TIMEOUT,
        json={"api-key": "test", "name": "Bob"},
    )
    await take_async_client.post(
        url=ADD_USER_ROUTE,
        timeout=TIMEOUT,
        json={"api-key": "second-test", "name": "Pit"},
    )
