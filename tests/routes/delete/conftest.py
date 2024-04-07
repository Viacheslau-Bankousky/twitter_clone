"""
This module contains async pytest fixtures for tweet-related activities.

These fixtures are designed to simulate actions on tweets such as adding a new
tweet without any media by a user, liking a tweet of a user, and subscribing
a second user for further interactions.
The process is done using an asynchronous HTTP client that performs different
POST requests for each fixture.

Modules:
--------
- `pytest_asyncio` to use asynchronous fixtures for testing asyncio
    Python code.
- `tests.helpers.values` for reference values used in the HTTP requests.
"""

import pytest_asyncio

from tests.helpers.values import (
    ROUTE_TO_LIKE_SPECIFIED_TWEET,
    SECOND_USER_ID,
    SUBSCRIPTION_ROUTE,
    TIMEOUT,
    TWEET_DATA_FIELD,
    TWEETS_ROUTE,
    VALUE_OF_TWEET_DATA_FIELD,
    base_header,
)


@pytest_asyncio.fixture(scope="function")
async def add_tweet_of_the_first_user_without_media(take_async_client) -> int:
    """
    Add a new tweet without any media by a user.

    This fixture posts a JSON tweet data to a specific route using an async
    HTTP client.
    The tweet data and route are defined in the `tests.helpers.values` module.
    The fixture then returns the ID of the newly added tweet.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.

    Returns:
        int: The ID of the newly added tweet.
    """
    tweet_response = await take_async_client.post(
        url=TWEETS_ROUTE,
        timeout=TIMEOUT,
        headers=base_header,
        json={
            TWEET_DATA_FIELD: VALUE_OF_TWEET_DATA_FIELD,
        },
    )
    return tweet_response.json().get("tweet_id")


@pytest_asyncio.fixture(scope="function")
async def add_like_of_user_tweet(
    take_async_client,
    add_tweet_of_the_first_user_without_media,
) -> int:
    """
     Add a like to a user's tweet.

     This fixture sends a POST request to a specific route that represents
     liking a tweet.
     It uses the ID of a tweet generated from the
     add_tweet_of_the_first_user_without_media fixture.
     It then returns the same tweet ID after adding the like.

    Args:
         take_async_client:
             Asynchronous client to perform HTTP requests.
         add_tweet_of_the_first_user_without_media (int):
             Tweet ID generated from the fixture that creates a new tweet
             for the first user.

    Returns:
         int: The ID of the liked tweet.
    """
    tweet_id: int = add_tweet_of_the_first_user_without_media
    await take_async_client.post(
        url=ROUTE_TO_LIKE_SPECIFIED_TWEET.format(tweet_id),
        timeout=TIMEOUT,
        headers=base_header,
    )
    return tweet_id


@pytest_asyncio.fixture(scope="function")
async def subscribe_the_second_user(take_async_client) -> None:
    """
    Subscribe a second user.

    This fixture sends a POST request to a specific subscription route.
    It uses an async HTTP client and headers from the `tests.helpers.values`
    module.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    await take_async_client.post(
        url=SUBSCRIPTION_ROUTE.format(SECOND_USER_ID),
        timeout=TIMEOUT,
        headers=base_header,
    )
