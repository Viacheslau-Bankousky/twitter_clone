"""
This module contains async pytests to verify deleting "Likes" of a tweet.

The process is done using an asynchronous HTTP client that performs
DELETE request for each test.
These tests involve interactions with tweet "Likes" including, confirming the
ability to delete a like of a tweet, ensuring non-existent likes cannot be
deleted, and assuring request is unsuccessful when the tweet 'like' targeted
for deletion contains forbidden symbols.

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
    NON_EXISTENT_TWEET_ID,
    ROUTE_TO_LIKE_SPECIFIED_TWEET,
    TIMEOUT,
    base_header,
)


@pytest.mark.asyncio
async def test_can_delete_like_of_the_tweet(
    take_async_client,
    add_like_of_user_tweet,
) -> None:
    """
    Check the ability of deletion a like of a specified tweet.

    This test will add a like to a tweet, then delete it,
    and verify the result using assertation checker.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
        add_like_of_user_tweet (int):
            Tweet ID generated from the fixture that creates a new like
            for a tweet.
            This like will be deleted in the test.
    """
    liked_tweet: int = add_like_of_user_tweet
    delete_like_response = await take_async_client.delete(
        ROUTE_TO_LIKE_SPECIFIED_TWEET.format(liked_tweet),
        timeout=TIMEOUT,
        headers=base_header,
    )
    positive_result_assertation_checker(
        response=delete_like_response,
        delete_instance=True,
    )


@pytest.mark.asyncio
async def test_cannot_delete_like_of_nonexistent_tweet(
    take_async_client,
) -> None:
    """
    Check if a non-existent like of a tweet cannot be deleted.

    This test will try to delete a like of a non-existent tweet,
    and verify the result using assertation checker.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    delete_like_response = await take_async_client.delete(
        ROUTE_TO_LIKE_SPECIFIED_TWEET.format(NON_EXISTENT_TWEET_ID),
        timeout=TIMEOUT,
        headers=base_header,
    )
    negative_result_assertation_checker(
        response=delete_like_response,
        error_type="bad request",
    )


@pytest.mark.asyncio
async def test_cannot_delete_like_of_the_wrong_tweet(
    take_async_client,
) -> None:
    """
    Check if the wrong or forbidden symbol like of a tweet cannot be deleted.

    This test will attempt to delete a like of a tweet where tweet ID contains
    forbidden symbols, and verify the result using assertation checker.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    delete_like_response = await take_async_client.delete(
        ROUTE_TO_LIKE_SPECIFIED_TWEET.format(FORBIDDEN_SYMBOL),
        timeout=TIMEOUT,
        headers=base_header,
    )
    negative_result_assertation_checker(
        response=delete_like_response,
        error_type="unprocessable entity",
    )
