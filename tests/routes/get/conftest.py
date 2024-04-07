"""
This module contains fixtures to set up an environment for GET routes.

This is done through the use of pytest fixtures, that once defined,
can be reused throughout the project, significantly simplifying the
setup and teardown of test environments.
These fixtures can also rely on each other to further extend their
functionality.

Modules:
--------
- pytest_asyncio: Plugin for pytest to test asyncio code.
- tests.helpers.helpers_for_media_adding: To provide media content for
    the tests.
- tests.helpers.values: To use predefined constants.

"""

import pytest_asyncio

from tests.helpers.helpers_for_media_adding import make_media_content
from tests.helpers.values import (
    MEDIAS_ROUTE,
    ROUTE_TO_LIKE_SPECIFIED_TWEET,
    SECOND_USER_ID,
    SUBSCRIPTION_ROUTE,
    TIMEOUT,
    TWEET_DATA_FIELD,
    TWEET_MEDIA_IDS_FIELD,
    TWEETS_ROUTE,
    USER_ID,
    VALUE_OF_TWEET_DATA_FIELD,
    base_header,
    base_header_for_the_second_user,
)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def subscribe_users(take_async_client) -> None:
    """
    Create subscriptions between users.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    await take_async_client.post(
        url=SUBSCRIPTION_ROUTE.format(SECOND_USER_ID),
        timeout=TIMEOUT,
        headers=base_header,
    )
    await take_async_client.post(
        url=SUBSCRIPTION_ROUTE.format(USER_ID),
        timeout=TIMEOUT,
        headers=base_header_for_the_second_user,
    )


@pytest_asyncio.fixture(scope="function", autouse=True)
async def add_tweet_of_the_second_user_with_media(take_async_client) -> int:
    """
    Tweet a new media post.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.

    Returns:
        int: The ID of the created tweet.
    """
    media_response = await take_async_client.post(
        url=MEDIAS_ROUTE,
        files=await make_media_content(),
        headers=base_header_for_the_second_user,
        timeout=TIMEOUT,
    )
    media_id: int = media_response.json().get("media_id")
    tweet_response = await take_async_client.post(
        url=TWEETS_ROUTE,
        timeout=TIMEOUT,
        headers=base_header_for_the_second_user,
        json={
            TWEET_DATA_FIELD: VALUE_OF_TWEET_DATA_FIELD,
            TWEET_MEDIA_IDS_FIELD: [media_id],
        },
    )
    return tweet_response.json().get("tweet_id")


@pytest_asyncio.fixture(scope="function", autouse=True)
async def add_like_of_the_tweet_of_the_second_user(
    take_async_client,
    add_tweet_of_the_second_user_with_media,
) -> None:
    """
    Like a tweeted media post.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
        add_tweet_of_the_second_user_with_media (int):
            Tweet ID generated from the fixture that creates a new tweet
            with media.
            This tweet will be liked in the test.
    """
    tweet_id: int = add_tweet_of_the_second_user_with_media
    await take_async_client.post(
        url=ROUTE_TO_LIKE_SPECIFIED_TWEET.format(tweet_id),
        timeout=TIMEOUT,
        headers=base_header,
    )
