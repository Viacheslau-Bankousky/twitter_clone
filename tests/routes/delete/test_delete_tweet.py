"""
This module contains async pytests to verify deleting "tweets".

The process is done using an asynchronous HTTP client that performs
DELETE requests for each test.
These tests involve interactions with tweets, including the ability
to delete a specified tweet, ensuring non-existent tweets cannot be
deleted, and verifying unsuccessful deletions when the tweet id
contains forbidden symbols.

Modules:
--------
- `pytest` to perform assertions for testing Python code.
- `tests.helpers.assertation_checker` for ensuring response from the
    requests is as expected.
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
    ROUTE_TO_DELETE_TWEET,
    TIMEOUT,
    base_header,
)


@pytest.mark.asyncio
async def test_can_delete_specified_tweet(
    take_async_client,
    add_tweet_of_the_first_user_without_media,
) -> None:
    """
    Check the ability to delete a specified tweet.

    This test will add a tweet, then delete it,
    and verify the result using assertation checker.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
        add_tweet_of_the_first_user_without_media (int):
            Tweet ID generated from the fixture that creates a new tweet.
            This tweet will be deleted in the test.
    """
    tweet_id: int = add_tweet_of_the_first_user_without_media
    delete_tweet_response = await take_async_client.delete(
        ROUTE_TO_DELETE_TWEET.format(tweet_id),
        timeout=TIMEOUT,
        headers=base_header,
    )
    positive_result_assertation_checker(
        response=delete_tweet_response,
        delete_instance=True,
    )


@pytest.mark.asyncio
async def test_cannot_delete_nonexistent_tweet(take_async_client) -> None:
    """
    Check if a non-existent tweet cannot be deleted.

    This test will try to delete a non-existent tweet,
    and verify the result using assertation checker.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    delete_tweet_response = await take_async_client.delete(
        ROUTE_TO_DELETE_TWEET.format(NON_EXISTENT_TWEET_ID),
        timeout=TIMEOUT,
        headers=base_header,
    )
    negative_result_assertation_checker(
        response=delete_tweet_response,
        error_type="bad request",
    )


@pytest.mark.asyncio
async def test_cannot_delete_tweet_with_wrong_symbol(
    take_async_client,
) -> None:
    """
    Check if the tweet with a wrong symbol cannot be deleted.

    This test will attempt to delete a tweet where tweet id contains
    forbidden symbols, and verify the result using assertation checker.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    delete_tweet_response = await take_async_client.delete(
        ROUTE_TO_DELETE_TWEET.format(FORBIDDEN_SYMBOL),
        timeout=TIMEOUT,
        headers=base_header,
    )
    negative_result_assertation_checker(
        response=delete_tweet_response,
        error_type="unprocessable entity",
    )
