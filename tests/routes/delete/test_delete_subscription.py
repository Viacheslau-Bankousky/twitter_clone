"""
This module contains async pytests to verify deleting user "subscriptions".

The process is done using an asynchronous HTTP client that performs
DELETE requests for each test.
These tests involve interactions with user "subscriptions" including confirming
the ability to delete a user subscription, ensuring non-existent subscriptions
cannot be deleted, assuring request is unsuccessful when the subscription user
ID contains forbidden symbols, and verifying unsuccessful attempts for
self-subscription deletions.

Modules:
--------
- `pytest` to perform assertions for testing Python code.
- `tests.helpers.assertation_checker` for ensuring response from the requests
    is as expected.
- `tests.helpers.values` to use defined constants for requests.

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
async def test_can_delete_user_subscription(
    take_async_client,
    subscribe_the_second_user,
) -> None:
    """
    Check the ability to delete a subscription for a specified user.

    This test will subscribe to a user, then delete the subscription,
    and verify the result using assertation checker.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
        subscribe_the_second_user:
            The ID of the second user obtained from the fixture used for
            creating new user subscriptions.
            This subscription will be deleted in this test.
    """
    delete_subscription_response = await take_async_client.delete(
        SUBSCRIPTION_ROUTE.format(SECOND_USER_ID),
        timeout=TIMEOUT,
        headers=base_header,
    )
    positive_result_assertation_checker(
        response=delete_subscription_response,
        delete_instance=True,
    )


@pytest.mark.asyncio
async def test_cannot_delete_nonexistent_subscription(
    take_async_client,
) -> None:
    """
    Check if a non-existent subscription cannot be deleted.

    This test will try to delete a subscription of a non-existent user,
    and verify the result using assertation checker.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    delete_subscription_response = await take_async_client.delete(
        SUBSCRIPTION_ROUTE.format(NON_EXISTENT_USER_ID),
        timeout=TIMEOUT,
        headers=base_header,
    )
    negative_result_assertation_checker(
        response=delete_subscription_response,
        error_type="bad request",
    )


@pytest.mark.asyncio
async def test_cannot_delete_self_subscription(
    take_async_client,
) -> None:
    """
    Verify unsuccessful attempts for deleting a self-subscription.

    This test ensures that users cannot delete their own subscriptions
    and verify the result using assertation checker.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    delete_subscription_response = await take_async_client.delete(
        SUBSCRIPTION_ROUTE.format(USER_ID),
        timeout=TIMEOUT,
        headers=base_header,
    )
    negative_result_assertation_checker(
        response=delete_subscription_response,
        error_type="bad request",
    )


@pytest.mark.asyncio
async def test_cannot_delete_wrong_user_subscription(
    take_async_client,
) -> None:
    """
    Check if the subscription of a user with a wrong ID cannot be deleted.

    This test will attempt to delete a subscription of a user where user
    ID contains forbidden symbols, and verify the result using assertation
    checker.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    delete_subscription_response = await take_async_client.delete(
        SUBSCRIPTION_ROUTE.format(FORBIDDEN_SYMBOL),
        timeout=TIMEOUT,
        headers=base_header,
    )
    negative_result_assertation_checker(
        response=delete_subscription_response,
        error_type="unprocessable entity",
    )
