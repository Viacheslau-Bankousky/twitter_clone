"""
This module contains async tests for adding tweets.

Imports:
--------
- pytest: For creating unit tests.
- tests.helpers.assertation_checker: For checking the server's
    responses.
- tests.helpers.values: To use predefined constants.

"""

import pytest

from tests.helpers.assertation_checker import (
    negative_result_assertation_checker,
    positive_result_assertation_checker,
)
from tests.helpers.values import (
    FORBIDDEN_SYMBOL,
    NONEXISTENT_MEDIA_ID,
    TIMEOUT,
    TWEET_DATA_FIELD,
    TWEET_MEDIA_IDS_FIELD,
    TWEETS_ROUTE,
    VALUE_OF_TWEET_DATA_FIELD,
    WRONG_VALUE_OF_TWEET_DATA_FIELD,
    base_header,
)


@pytest.mark.asyncio
async def test_can_add_tweet_without_media(take_async_client) -> None:
    """
    Check a possibility to add a tweet without media.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    response = await take_async_client.post(
        TWEETS_ROUTE,
        timeout=TIMEOUT,
        headers=base_header,
        json={TWEET_DATA_FIELD: VALUE_OF_TWEET_DATA_FIELD},
    )
    positive_result_assertation_checker(
        response=response,
        created_instance="tweet_id",
    )


@pytest.mark.asyncio
async def test_can_add_tweet_with_media(
    take_async_client,
    add_new_media_for_the_tweet_of_the_first_user,
) -> None:
    """
    Check a possibility to add a tweet with media.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
        add_new_media_for_the_tweet_of_the_first_user:
            Fixture for adding new media for a tweet.
    """
    media_id: int = add_new_media_for_the_tweet_of_the_first_user
    tweet_response = await take_async_client.post(
        url=TWEETS_ROUTE,
        timeout=TIMEOUT,
        headers=base_header,
        json={
            TWEET_DATA_FIELD: VALUE_OF_TWEET_DATA_FIELD,
            TWEET_MEDIA_IDS_FIELD: [media_id],
        },
    )
    positive_result_assertation_checker(
        response=tweet_response,
        created_instance="tweet_id",
    )


@pytest.mark.asyncio
async def test_cannot_add_tweet_without_data(take_async_client) -> None:
    """
    Check an impossibility to add a tweet without any data.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    response = await take_async_client.post(
        url=TWEETS_ROUTE,
        timeout=TIMEOUT,
        headers=base_header,
    )
    negative_result_assertation_checker(
        response=response,
        error_type="unprocessable entity",
    )


@pytest.mark.asyncio
async def test_cannot_add_tweet_with_wrong_data(take_async_client) -> None:
    """
    Check an impossibility to add a tweet with the wrong data.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    response = await take_async_client.post(
        url=TWEETS_ROUTE,
        timeout=TIMEOUT,
        headers=base_header,
        json={
            TWEET_DATA_FIELD: WRONG_VALUE_OF_TWEET_DATA_FIELD,
        },
    )
    negative_result_assertation_checker(
        response=response,
        error_type="unprocessable entity",
    )


@pytest.mark.asyncio
async def test_cannot_add_tweet_with_nonexistent_media_ids(  # noqa: WPS118
    take_async_client,
) -> None:
    """
    Check an impossibility to add a tweet with all nonexistent media ids.

     Args:
         take_async_client: Asynchronous client to perform HTTP requests.
    """
    response = await take_async_client.post(
        TWEETS_ROUTE,
        timeout=TIMEOUT,
        headers=base_header,
        json={
            TWEET_DATA_FIELD: VALUE_OF_TWEET_DATA_FIELD,
            TWEET_MEDIA_IDS_FIELD: [NONEXISTENT_MEDIA_ID],
        },
    )
    negative_result_assertation_checker(
        response=response,
        error_type="bad request",
    )


@pytest.mark.asyncio
async def test_cannot_add_tweet_with_one_nonexistent_media_id(  # noqa: WPS118
    take_async_client,
    add_new_media_for_the_tweet_of_the_first_user,
) -> None:
    """
    Check an impossibility to add a tweet with one nonexistent media ID.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
        add_new_media_for_the_tweet_of_the_first_user:
            Fixture for adding new media for the tweet.
    """
    media_id: int = add_new_media_for_the_tweet_of_the_first_user
    response = await take_async_client.post(
        TWEETS_ROUTE,
        timeout=TIMEOUT,
        headers=base_header,
        json={
            TWEET_DATA_FIELD: VALUE_OF_TWEET_DATA_FIELD,
            TWEET_MEDIA_IDS_FIELD: [media_id, NONEXISTENT_MEDIA_ID],
        },
    )
    negative_result_assertation_checker(
        response=response,
        error_type="bad request",
    )


@pytest.mark.asyncio
async def test_cannot_add_tweet_with_wrong_media_id(
    take_async_client,
    add_new_media_for_the_tweet_of_the_first_user,
) -> None:
    """
    Check an impossibility to add a tweet with a wrong media ID.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
        add_new_media_for_the_tweet_of_the_first_user:
            Fixture for adding new media for the tweet.
    """
    media_id: int = add_new_media_for_the_tweet_of_the_first_user
    response = await take_async_client.post(
        TWEETS_ROUTE,
        timeout=TIMEOUT,
        headers=base_header,
        json={
            TWEET_DATA_FIELD: VALUE_OF_TWEET_DATA_FIELD,
            TWEET_MEDIA_IDS_FIELD: [FORBIDDEN_SYMBOL, media_id],
        },
    )
    negative_result_assertation_checker(
        response=response,
        error_type="unprocessable entity",
    )
