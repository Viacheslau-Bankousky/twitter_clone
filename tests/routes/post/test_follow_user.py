"""
This module contains async tests for the user subscription.

Imports:
--------
- pytest: A testing framework that allows to easily create small,
    simple tests.
- tests.helpers.assertion_checker: Contains helper functions to
    check assertions.
- tests.helpers.values: Predefined constants used in requests.

"""

import pytest

from tests.helpers.assertation_checker import (
    negative_result_assertation_checker,
    positive_result_assertation_checker,
)
from tests.helpers.values import (
    FORBIDDEN_SYMBOL,
    NON_EXISTENT_USER_ID,
    SECOND_USER_ID,
    SUBSCRIPTION_ROUTE,
    TIMEOUT,
    USER_ID,
    base_header,
)


@pytest.mark.asyncio
async def can_subscribe_user(take_async_client) -> None:
    """
    Test the functionality of a user subscribing to another user's posts.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    subscription_response = await take_async_client.post(
        url=SUBSCRIPTION_ROUTE.format(SECOND_USER_ID),
        timeout=TIMEOUT,
        headers=base_header,
    )
    positive_result_assertation_checker(response=subscription_response)


@pytest.mark.asyncio
async def cannot_subscribe_nonexistent_user(take_async_client) -> None:
    """
    Test handling of an attempt to subscribe to a non-existent user.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    subscription_response = await take_async_client.post(
        url=SUBSCRIPTION_ROUTE.format(NON_EXISTENT_USER_ID),
        timeout=TIMEOUT,
        headers=base_header,
    )
    negative_result_assertation_checker(
        response=subscription_response,
        error_type="bad request",
    )


@pytest.mark.asyncio
async def cannot_get_self_subscription(take_async_client) -> None:
    """
    Test the constrains of a user trying to subscribe to their own posts.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    subscription_response = await take_async_client.post(
        url=SUBSCRIPTION_ROUTE.format(USER_ID),
        timeout=TIMEOUT,
        headers=base_header,
    )
    negative_result_assertation_checker(
        response=subscription_response,
        error_type="bad request",
    )


@pytest.mark.asyncio
async def cannot_subscribe_user_with_forbidden_symbol(
    take_async_client,
) -> None:
    """
    Test error handling when the symbols used for subscription are forbidden.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    subscription_response = await take_async_client.post(
        url=SUBSCRIPTION_ROUTE.format(FORBIDDEN_SYMBOL),
        timeout=TIMEOUT,
        headers=base_header,
    )
    negative_result_assertation_checker(
        response=subscription_response,
        error_type="unprocessable entity",
    )
