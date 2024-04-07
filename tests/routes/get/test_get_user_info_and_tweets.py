"""
This module contains async pytests to verify fetching user info.

The verification is done performing GET requests for each test.
These tests involve interactions with specified user info and tweets
of the current user, including the ability to get specified user
by USER_ID, get info of the current user, ensure info of non-existent
users cannot be gotten, and check if it's possible to get the tweets
from the current user, also ensuring that user with wrong id cannot
be fetched.

Modules:
--------
- pytest: to perform assertions for testing Python code.
- tests.helpers.assertation_checker: for ensuring response from the
    requests is as expected.
- tests.helpers.values: to use defined constants for requests.

"""

from typing import List

import pytest

from tests.helpers.assertation_checker import (
    negative_result_assertation_checker,
    user_info_assertation_checker,
    user_tweets_assertation_checker,
)
from tests.helpers.values import (
    FORBIDDEN_SYMBOL,
    NON_EXISTENT_USER_ID,
    SPECIFIED_USER_INFO_ROUTE,
    TIMEOUT,
    TWEETS_ROUTE,
    USER_ID,
    USER_INFO_ROUTE,
    base_header,
)

test_data: List[str] = [
    SPECIFIED_USER_INFO_ROUTE.format(USER_ID),
    USER_INFO_ROUTE,
]


@pytest.mark.asyncio
@pytest.mark.parametrize("route", test_data)
async def test_can_get_current_user_and_user_by_id(
    take_async_client,
    route: str,
) -> None:
    """
    Check the ability to get user info.

    This test will get the user info both by user's ID and for the current
    user, and verify the result using assertation checker.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
        route (str):
            The url route used to perform the GET request.
    """
    response = await take_async_client.get(
        url=route,
        timeout=TIMEOUT,
        headers=base_header,
    )
    user_info_assertation_checker(response=response)


@pytest.mark.asyncio
async def test_cannot_get_non_existent_user(take_async_client) -> None:
    """
    Check if a non-existent user cannot be gotten.

    This test will try to get info of a non-existent user,
    and verify the result using assertation checker.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    response = await take_async_client.get(
        url=SPECIFIED_USER_INFO_ROUTE.format(NON_EXISTENT_USER_ID),
        timeout=TIMEOUT,
        headers=base_header,
    )
    negative_result_assertation_checker(
        response=response,
        error_type="bad request",
    )


@pytest.mark.asyncio
async def test_cannot_get_user_with_wrong_id(
    take_async_client,
) -> None:
    """
    Check if the user with a wrong id cannot be gotten.

    This test will get info of user with id contains
    forbidden symbols, and verify the result using
    assertation checker.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    response = await take_async_client.get(
        url=SPECIFIED_USER_INFO_ROUTE.format(FORBIDDEN_SYMBOL),
        timeout=TIMEOUT,
        headers=base_header,
    )
    negative_result_assertation_checker(
        response=response,
        error_type="unprocessable entity",
    )


@pytest.mark.asyncio
async def test_can_get_tweets_of_current_user(take_async_client) -> None:
    """
    Check if tweets of the current user can be gotten.

    This test will get tweets of the current user, and verify the result
    using assertation checker.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    response = await take_async_client.get(
        TWEETS_ROUTE,
        timeout=TIMEOUT,
        headers=base_header,
    )
    user_tweets_assertation_checker(response=response)
