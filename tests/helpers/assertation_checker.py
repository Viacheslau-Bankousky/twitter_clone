"""
This module provides assertions for checking responses during testing.

These functions are used in tests to validate the responses we receive
from the API during testing.
Specifically, we check the status codes, data structure types and data content.

Modules:
--------
- `httpx` for `Response` type
- `typing` for optional and type hinting
- `tests.helpers.values` for reference values

"""

from typing import Dict, Optional

from httpx import Response

from tests.helpers.values import (
    ADDED_STATUS_CODE,
    BAD_REQUEST_STATUS_CODE,
    INTERNAL_ERROR_STATUS_CODE,
    SUCCESS_RESULT,
    SUCCESS_STATUS_CODE,
    UNPROCESSABLE_ENTITY_CODE,
    UNSUCCESSFUL_RESULT,
)


def negative_result_assertation_checker(
    response: Response,
    error_type: str,
) -> None:
    """
    Check a negative responses.

    Checks if the HTTP response code matches the expected status
    and if the response JSON contains the expected error fields.

    Args:
        response (Response):
            HTTP response object.
        error_type (str):
            The expected error type.
    """
    if error_type == "bad request":
        assert response.status_code == BAD_REQUEST_STATUS_CODE
    if error_type == "unprocessable entity":
        assert response.status_code == UNPROCESSABLE_ENTITY_CODE
    if error_type == "internal server error":
        assert response.status_code == INTERNAL_ERROR_STATUS_CODE

    response_json: Dict = response.json()
    assert response_json.get("result") == UNSUCCESSFUL_RESULT
    assert isinstance(response_json.get("error_type"), str)
    assert isinstance(response_json.get("error_message"), str)


def positive_result_assertation_checker(
    response: Response,
    delete_instance=False,
    created_instance: Optional[str] = None,
) -> None:
    """
    Check a positive responses.

    Checks if the HTTP response code matches the expected status
    and if the response JSON contains the expected successful fields.

    Args:
        response (Response):
            HTTP response object.
        delete_instance (bool):
            Flag if operation was a delete.
        created_instance (Optional[str]):
            Instance type that should be created.
    """
    assert (
        response.status_code == SUCCESS_STATUS_CODE  # noqa: WPS444
        if delete_instance
        else ADDED_STATUS_CODE
    )
    response_json: Dict = response.json()
    assert response_json.get("result") == SUCCESS_RESULT
    if created_instance:
        assert isinstance(response_json.get(created_instance), int)


def user_info_assertation_checker(response: Response) -> None:
    """
    Check user information responses.

    Args:
        response (Response):
            HTTP response object.
    """
    assert response.status_code == SUCCESS_STATUS_CODE
    response_json: Dict = response.json()
    assert response_json.get("result") == SUCCESS_RESULT
    assert isinstance(response_json.get("user"), dict)
    user: Dict = response_json.get("user")  # type: ignore
    assert isinstance(user.get("id"), int)
    assert isinstance(user.get("name"), str)
    assert isinstance(
        user.get("followers")[0].get("id"),  # type: ignore
        int,
    )
    assert isinstance(
        user.get("following")[0].get("name"),  # type: ignore
        str,
    )


def user_tweets_assertation_checker(response: Response) -> None:
    """
    Check user tweets responses.

    Args:
        response (Response):
            HTTP response object.
    """
    assert response.status_code == SUCCESS_STATUS_CODE
    response_json: Dict = response.json()
    assert response_json.get("result") == SUCCESS_RESULT
    tweets: Dict = response_json.get("tweets")  # type: ignore
    assert isinstance(tweets, list)
    tweet_data: Dict = tweets[0]
    assert isinstance(tweet_data, dict)
    assert isinstance(tweet_data.get("id"), int)
    assert isinstance(tweet_data.get("content"), str)
    assert isinstance(tweet_data.get("attachments"), list)
    assert isinstance(
        tweets[0].get("attachments")[0],
        str,
    )
    author: Dict = tweet_data.get("author")
    assert isinstance(author, dict)
    assert isinstance(author.get("id"), int)
    assert isinstance(author.get("name"), str)
    likes: list = tweet_data.get("likes")
    assert isinstance(likes, list)
    assert isinstance(likes[0], dict)
    assert isinstance(likes[0].get("id"), int)
    assert isinstance(likes[0].get("name"), str)
