"""
This module contains async tests for media upload functionality.

Imports:
--------
- pytest: For creating unit tests.
- tests.helpers.assertation_checker: For checking the server's responses.
- tests.helpers.helpers_for_media_adding: Provides helper functions for
    preparing media data.
- tests.helpers.values: To use predefined constants.

"""

import pytest

from tests.helpers.assertation_checker import (
    negative_result_assertation_checker,
    positive_result_assertation_checker,
)
from tests.helpers.helpers_for_media_adding import (
    make_media_content,
    make_wrong_media_content,
)
from tests.helpers.values import MEDIAS_ROUTE, TIMEOUT, base_header


@pytest.mark.asyncio
async def test_can_add_media(
    take_async_client,
) -> None:
    """
    Check a possibility to upload a correct media file.

     Args:
         take_async_client:
             Asynchronous client to perform HTTP requests.
    """
    media_response = await take_async_client.post(
        url=MEDIAS_ROUTE,
        timeout=TIMEOUT,
        headers=base_header,
        files=await make_media_content(),
    )
    positive_result_assertation_checker(
        response=media_response,
        created_instance="media_id",
    )


@pytest.mark.asyncio
async def test_cannot_add_wrong_media(
    take_async_client,
) -> None:
    """
    Check a possibility to upload a wrong media file.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    media_response = await take_async_client.post(
        url=MEDIAS_ROUTE,
        timeout=TIMEOUT,
        headers=base_header,
        files=await make_wrong_media_content(
            file_path="../../../README.md",
            file_type="text/markdown",
        ),
    )
    negative_result_assertation_checker(
        response=media_response,
        error_type="bad request",
    )


@pytest.mark.asyncio
async def test_cannot_add_empty_media(
    take_async_client,
) -> None:
    """
    Check whether an empty media file cannot be uploaded.

    Args:
        take_async_client:
            Asynchronous client to perform HTTP requests.
    """
    media_response = await take_async_client.post(
        url=MEDIAS_ROUTE,
        timeout=TIMEOUT,
        headers=base_header,
    )
    negative_result_assertation_checker(
        response=media_response,
        error_type="unprocessable entity",
    )
