"""
This module contains async pytests for testing tweet liking functionality.

Modules:
--------
- pytest:  To perform assertions for testing Python code.
- tests.helpers.assertation_checker:  For ensuring response from the requests
    is as expected.
- tests.helpers.values: To use predefined constants for requests.

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
async def test_can_add_like_of_the_tweet(
    take_async_client,
    add_tweet_of_the_second_user_without_media,
) -> None:
    """
    Check whether user can like a tweet.

    Args:
        take_async_client:
            Async test client.
        add_tweet_of_the_second_user_without_media:
            Fixture that creates a tweet by the second user.
    """
    tweet_id: int = add_tweet_of_the_second_user_without_media
    like_response = await take_async_client.post(
        url=ROUTE_TO_LIKE_SPECIFIED_TWEET.format(tweet_id),
        timeout=TIMEOUT,
        headers=base_header,
    )
    positive_result_assertation_checker(response=like_response)


@pytest.mark.asyncio
async def test_cannot_add_like_of_the_nonexistent_tweet(
    take_async_client,
) -> None:
    """
    Check whether user cannot like a non-existent tweet.

    Args:
        take_async_client: Async test client.
    """
    like_response = await take_async_client.post(
        url=ROUTE_TO_LIKE_SPECIFIED_TWEET.format(NON_EXISTENT_TWEET_ID),
        timeout=TIMEOUT,
        headers=base_header,
    )
    negative_result_assertation_checker(
        response=like_response,
        error_type="bad request",
    )


@pytest.mark.asyncio
async def test_cannot_add_like_with_wrong_symbol(
    take_async_client,
) -> None:
    """
    Check whether user cannot use a wrong symbol in the like request.

    Args:
        take_async_client: Async test client.
    """
    like_response = await take_async_client.post(
        url=ROUTE_TO_LIKE_SPECIFIED_TWEET.format(FORBIDDEN_SYMBOL),
        timeout=TIMEOUT,
        headers=base_header,
    )
    negative_result_assertation_checker(
        response=like_response,
        error_type="unprocessable entity",
    )
