"""
This module contains async pytest fixtures for tweet-related testing.

These fixtures facilitate efficient setup and teardown processes for tests.

Imports:
--------
- pytest_asyncio: For asynchronous interaction with pytest.
- tests.helpers.helpers_for_media_adding: For generating media content needed
    for the tests.
- tests.helpers.values: To use defined constants for the tests.

"""

import pytest_asyncio

from tests.helpers.helpers_for_media_adding import make_media_content
from tests.helpers.values import (
    MEDIAS_ROUTE,
    TIMEOUT,
    TWEET_DATA_FIELD,
    TWEETS_ROUTE,
    VALUE_OF_TWEET_DATA_FIELD,
    base_header,
    base_header_for_the_second_user,
)


@pytest_asyncio.fixture(scope="function")
async def add_new_media_for_the_tweet_of_the_first_user(
    take_async_client,
) -> int:
    """
    Post a new media and return its id.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.

    Returns:
        int: The ID of the posted media.
    """
    response = await take_async_client.post(
        url=MEDIAS_ROUTE,
        files=await make_media_content(),
        headers=base_header,
        timeout=TIMEOUT,
    )
    response_data = response.json()
    return response_data.get("media_id")


@pytest_asyncio.fixture(scope="function", autouse=True)
async def add_tweet_of_the_second_user_without_media(take_async_client) -> int:
    """
    Post a new tweet without media and return its id.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.

    Returns:
        int: The ID of the posted tweet.
    """
    tweet_response = await take_async_client.post(
        url=TWEETS_ROUTE,
        timeout=TIMEOUT,
        headers=base_header_for_the_second_user,
        json={
            TWEET_DATA_FIELD: VALUE_OF_TWEET_DATA_FIELD,
        },
    )
    return tweet_response.json().get("tweet_id")
