"""
This module contains async pytests that test the adding a new user.

Imports:
--------
- pytest: For creating unit tests.
- tests.helpers.assertation_checker: For checking server responses.
- tests.helpers.values: Predefined constants used in requests.

"""

import pytest

from tests.helpers.assertation_checker import (
    negative_result_assertation_checker,
    positive_result_assertation_checker,
)
from tests.helpers.values import (
    ADD_USER_ROUTE,
    NAME_FIELD,
    TESTING_API_KEY_FIELD,
    TIMEOUT,
    VALUE_OF_NAME_FIELD,
    VALUE_OF_TESTING_API_KEY_FIELD,
    WRONG_VALUE_OF_NAME_FIELD,
    WRONG_VALUE_OF_TESTING_API_KEY_FIELD,
)


@pytest.mark.asyncio
async def test_can_add_new_user(take_async_client) -> None:
    """
    Check a possibility to add new user with correct credentials.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    user_response = await take_async_client.post(
        url=ADD_USER_ROUTE,
        timeout=TIMEOUT,
        json={
            TESTING_API_KEY_FIELD: VALUE_OF_TESTING_API_KEY_FIELD,
            NAME_FIELD: VALUE_OF_NAME_FIELD,
        },
    )
    positive_result_assertation_checker(
        response=user_response,
        created_instance="id",
    )


@pytest.mark.asyncio
async def test_cannot_add_new_user_without_name(take_async_client) -> None:
    """
    Check an impossibility to add new user without providing a name.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    user_response = await take_async_client.post(
        url=ADD_USER_ROUTE,
        timeout=TIMEOUT,
        json={TESTING_API_KEY_FIELD: VALUE_OF_TESTING_API_KEY_FIELD},
    )
    negative_result_assertation_checker(
        response=user_response,
        error_type="unprocessable entity",
    )


@pytest.mark.asyncio
async def test_cannot_add_new_user_with_wrong_name(take_async_client) -> None:
    """
    Check an impossibility to add new user with an incorrect name.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    user_response = await take_async_client.post(
        url=ADD_USER_ROUTE,
        timeout=TIMEOUT,
        json={
            TESTING_API_KEY_FIELD: VALUE_OF_TESTING_API_KEY_FIELD,
            NAME_FIELD: WRONG_VALUE_OF_NAME_FIELD,
        },
    )
    negative_result_assertation_checker(
        response=user_response,
        error_type="unprocessable entity",
    )


@pytest.mark.asyncio
async def test_cannot_add_new_user_with_empty_api_key(
    take_async_client,
) -> None:
    """
    Check an impossibility to add new user without providing an API key.

    Args:
        take_async_client:
            Async test client.
    """
    user_response = await take_async_client.post(
        url=ADD_USER_ROUTE,
        timeout=TIMEOUT,
        json={NAME_FIELD: VALUE_OF_NAME_FIELD},
    )
    negative_result_assertation_checker(
        response=user_response,
        error_type="unprocessable entity",
    )


@pytest.mark.asyncio
async def test_cannot_add_new_user_with_wrong_api_key(
    take_async_client,
) -> None:
    """
    Check an impossibility to add new user with an incorrect API key.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    user_response = await take_async_client.post(
        url=ADD_USER_ROUTE,
        timeout=TIMEOUT,
        json={
            TESTING_API_KEY_FIELD: WRONG_VALUE_OF_TESTING_API_KEY_FIELD,
            NAME_FIELD: VALUE_OF_NAME_FIELD,
        },
    )
    negative_result_assertation_checker(
        response=user_response,
        error_type="unprocessable entity",
    )
