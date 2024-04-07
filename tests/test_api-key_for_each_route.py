"""
This module contains test cases for the application's routes.

It uses the `pytest` framework and asynchronous test cases to
verify that:
- Data cannot be retrieved or added without an API key.
- Data cannot be retrieved or added with a wrong API key.
- Data cannot be deleted without an API key.
- Data cannot be deleted with a wrong API key.

It calls utilities from `tests.helpers`, and uses test data to
iterate through each route.
Test data for GET, POST and DELETE requests are stored in
`test_data_for_get_routes`, `test_data_for_post_routes` and
`test_data_for_delete_routes` respectively.

Modules:
--------
typing: For collection typecasting, and to provide hints for functions
pytest: The testing framework being used
tests.helpers.assertation_checker: For validating responses
tests.helpers.helpers_for_media_adding: To help create media content
for testing
tests.helpers.values: Contains route and key-value pairs of data

"""
from typing import List

import pytest

from tests.helpers.assertation_checker import (
    negative_result_assertation_checker,
)
from tests.helpers.helpers_for_media_adding import make_media_content
from tests.helpers.values import (
    MEDIAS_ROUTE,
    ROUTE_TO_DELETE_TWEET,
    ROUTE_TO_LIKE_SPECIFIED_TWEET,
    SPECIFIED_USER_INFO_ROUTE,
    SUBSCRIPTION_ROUTE,
    TIMEOUT,
    TWEET_DATA_FIELD,
    TWEETS_ROUTE,
    USER_ID,
    USER_INFO_ROUTE,
    VALUE_OF_TWEET_DATA_FIELD,
    wrong_header,
)

test_data_for_get_routes: List[str] = [
    SPECIFIED_USER_INFO_ROUTE.format(USER_ID),
    USER_INFO_ROUTE,
    TWEETS_ROUTE,
]

test_data_for_post_routes: List[str] = [
    TWEETS_ROUTE,
    MEDIAS_ROUTE,
    ROUTE_TO_LIKE_SPECIFIED_TWEET,
    SUBSCRIPTION_ROUTE,
]

test_data_for_delete_routes: List[str] = [
    ROUTE_TO_DELETE_TWEET,
    SUBSCRIPTION_ROUTE,
    ROUTE_TO_LIKE_SPECIFIED_TWEET,
]


@pytest.mark.asyncio
@pytest.mark.parametrize("route", test_data_for_get_routes)
async def test_cannot_get_data_without_api_key(
    take_async_client,
    route: str,
) -> None:
    """
    Verify that data cannot be retrieved without an API key.

    Args:
        take_async_client (fixture):
            Fixture that provides a simulation of an asynchronous client.
        route (str):
            The route being tested.

    Return:
        Nothing.
        If the test passes, it means that the application correctly denies
        unauthenticated requests.
    """
    response = await take_async_client.get(url=route, timeout=TIMEOUT)
    negative_result_assertation_checker(
        response=response,
        error_type="internal server error",
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("route", test_data_for_get_routes)
async def test_cannot_get_data_with_wrong_api_key(
    take_async_client,
    route: str,
) -> None:
    """
    Verify that data cannot be retrieved with a wrong API key.

    Args:
        take_async_client (fixture):
            Fixture that provides a simulation of an asynchronous client.
        route (str):
            The route being tested.

    Return:
        Nothing.
        If the test passes, it means that the application correctly denies
        requests with wrong API keys.
    """
    response = await take_async_client.get(
        url=route,
        timeout=TIMEOUT,
        headers=wrong_header,
    )
    negative_result_assertation_checker(
        response=response,
        error_type="internal server error",
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("route", test_data_for_post_routes)
async def test_cannot_add_data_without_api_key(
    take_async_client,
    route: str,
) -> None:
    """
    Verify that data cannot be added without an API key.

    Args:
        take_async_client (fixture):
            Fixture that provides a simulation of an asynchronous client.
        route (str):
            The route being tested.

    Return:
        Nothing.
        If the test passes, it means that the application correctly denies
        unauthenticated requests.
    """
    if route == TWEETS_ROUTE:
        response = await take_async_client.post(
            url=route,
            timeout=TIMEOUT,
            json=({TWEET_DATA_FIELD: VALUE_OF_TWEET_DATA_FIELD}),
        )
    else:
        response = await take_async_client.post(
            url=route,
            timeout=TIMEOUT,
            files=await make_media_content(),
        )
    negative_result_assertation_checker(
        response=response,
        error_type="internal server error",
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("route", test_data_for_post_routes)
async def test_cannot_add_data_with_wrong_api_key(
    take_async_client,
    route: str,
) -> None:
    """
    Verify that data cannot be added with a wrong API key.

    Args:
        take_async_client (fixture):
            Fixture that provides a simulation of an asynchronous client.
        route (str):
            The route being tested.

    Return:
        Nothing.
        If the test passes, it means that the application correctly denies
        requests with wrong API keys.
    """
    if route == TWEETS_ROUTE:
        response = await take_async_client.post(
            url=route,
            timeout=TIMEOUT,
            headers=wrong_header,
            json=({TWEET_DATA_FIELD: VALUE_OF_TWEET_DATA_FIELD}),
        )
    else:
        response = await take_async_client.post(
            url=route,
            timeout=TIMEOUT,
            headers=wrong_header,
            files=await make_media_content(),
        )
    negative_result_assertation_checker(
        response=response,
        error_type="internal server error",
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("route", test_data_for_delete_routes)
async def test_cannot_delete_data_without_api_key(
    take_async_client,
    route: str,
) -> None:
    """
    Verify that data cannot be deleted without an API key.

    Args:
        take_async_client (fixture):
            Fixture that provides a simulation of an asynchronous client.
        route (str):
            The route being tested.

    Return:
        Nothing.
        If the test passes, it means that the application correctly denies
        unauthenticated requests.
    """
    if route == TWEETS_ROUTE:
        response = await take_async_client.post(
            url=route,
            timeout=TIMEOUT,
            json=({TWEET_DATA_FIELD: VALUE_OF_TWEET_DATA_FIELD}),
        )
    else:
        response = await take_async_client.post(
            url=route,
            timeout=TIMEOUT,
            files=await make_media_content(),
        )
    negative_result_assertation_checker(
        response=response,
        error_type="internal server error",
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("route", test_data_for_delete_routes)
async def test_cannot_delete_data_with_wrong_api_key(
    take_async_client,
    route: str,
) -> None:
    """
    Verify that data cannot be deleted with a wrong API key.

    Args:
        take_async_client (fixture):
            Fixture that provides a simulation of an asynchronous client.
        route (str):
            The route being tested.

    Return:
        Nothing.
        If the test passes, it means that the application correctly denies
        requests with wrong API keys.
    """
    if route == TWEETS_ROUTE:
        response = await take_async_client.post(
            url=route,
            timeout=TIMEOUT,
            headers=wrong_header,
            json=({TWEET_DATA_FIELD: VALUE_OF_TWEET_DATA_FIELD}),
        )
    else:
        response = await take_async_client.post(
            url=route,
            timeout=TIMEOUT,
            headers=wrong_header,
            files=await make_media_content(),
        )
    negative_result_assertation_checker(
        response=response,
        error_type="internal server error",
    )
