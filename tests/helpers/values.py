"""
This module defines the constants and variables used for testing.

These constants are used to define request timeouts, URL paths,
status codes, API keys and other testing related constants.
These constants are used across multiple testing modules.

Variables:
----------
TIMEOUT: timeout for the request.
BASE_URL: base URL for the testing server.

ADDED_STATUS_CODE: HTTP status code for successful post request.
BAD_REQUEST_STATUS_CODE: HTTP status code for bad request.
UNPROCESSABLE_ENTITY_CODE: HTTP status code for unprocessable entity error.
INTERNAL_ERROR_STATUS_CODE: HTTP status code for internal server error.
SUCCESS_STATUS_CODE: HTTP status code for success response.

SUCCESS_RESULT: boolean for successful operation.
UNSUCCESSFUL_RESULT: boolean for unsuccessful operation.

base_header: dictionary containing the api-key for testing user.
wrong_header: dictionary containing the wrong api-key.
base_header_for_the_second_user: dictionary containing the api-key for the
second testing user.

TWEET_DATA_FIELD: field for tweet data.
VALUE_OF_TWEET_DATA_FIELD: value for tweet data field for testing.
WRONG_VALUE_OF_TWEET_DATA_FIELD: wrong value for tweet data field for testing.

TWEET_MEDIA_IDS_FIELD: field for tweet media ids.
MEDIAS_DATA_FIELD: field for media data

TESTING_API_KEY_FIELD: field for testing API key.
VALUE_OF_TESTING_API_KEY_FIELD: value for testing API key.
WRONG_VALUE_OF_TESTING_API_KEY_FIELD: wrong value for testing API key.

NAME_FIELD: field for user name.
VALUE_OF_NAME_FIELD: value for user name.
WRONG_VALUE_OF_NAME_FIELD: wrong value for user name.

WRONG_MEDIA_ID: wrong id for media for testing.
USER_ID: user id for testing.
NON_EXISTENT_USER_ID: non-existing user id for testing.
TWEET_ID: tweet id for testing.
NON_EXISTENT_TWEET_ID: non-existing tweet id for testing.

FORBIDDEN_SYMBOL: forbidden symbol in tweet id for testing.

TWEETS_ROUTE: endpoint for tweets collection.
ROUTE_TO_DELETE_TWEET: endpoint to delete a specific tweet.
MEDIAS_ROUTE: endpoint for medias collection.
ADD_USER_ROUTE: endpoint to add a new user.
SPECIFIED_USER_INFO_ROUTE: endpoint to get info of a specific user.
USER_INFO_ROUTE: endpoint to get info of the authenticated user.
SUBSCRIPTION_ROUTE: endpoint to subscribe to a user.
ROUTE_TO_LIKE_SPECIFIED_TWEET: endpoint to like a specified tweet.

"""
from typing import Dict

TIMEOUT: int = 5

BASE_URL: str = "http://test_nginx"

ADDED_STATUS_CODE: int = 201
BAD_REQUEST_STATUS_CODE: int = 400
UNPROCESSABLE_ENTITY_CODE: int = 422
INTERNAL_ERROR_STATUS_CODE: int = 500
SUCCESS_STATUS_CODE: int = 200

SUCCESS_RESULT: bool = True
UNSUCCESSFUL_RESULT: bool = False

base_header: Dict[str, str] = {"api-key": "test"}
wrong_header: Dict[str, str] = {"api-key": "wrong-test"}
base_header_for_the_second_user: Dict[str, str] = {"api-key": "second-test"}

TWEET_DATA_FIELD: str = "tweet_data"
VALUE_OF_TWEET_DATA_FIELD: str = "test_tweet_data"
WRONG_VALUE_OF_TWEET_DATA_FIELD: int = 1111

TWEET_MEDIA_IDS_FIELD: str = "tweet_media_ids"

MEDIAS_DATA_FIELD: str = "file"

TESTING_API_KEY_FIELD: str = "api-key"
VALUE_OF_TESTING_API_KEY_FIELD: str = "random_key"
WRONG_VALUE_OF_TESTING_API_KEY_FIELD: int = 1111
NAME_FIELD: str = "name"
VALUE_OF_NAME_FIELD: str = "random_user"
WRONG_VALUE_OF_NAME_FIELD: int = 1111

NONEXISTENT_MEDIA_ID: int = 1000
USER_ID: int = 1
SECOND_USER_ID: int = 2
NON_EXISTENT_USER_ID: int = 1000
TWEET_ID: int = 1
NON_EXISTENT_TWEET_ID: int = 1000

FORBIDDEN_SYMBOL: str = "("

TWEETS_ROUTE: str = "/api/tweets"
ROUTE_TO_DELETE_TWEET: str = "/api/tweets/{0}"
MEDIAS_ROUTE: str = "/api/medias"
ADD_USER_ROUTE: str = "/api/users/new"
SPECIFIED_USER_INFO_ROUTE: str = "/api/users/{0}"
USER_INFO_ROUTE: str = "/api/users/me"
SUBSCRIPTION_ROUTE: str = "/api/users/{0}/follow"
ROUTE_TO_LIKE_SPECIFIED_TWEET: str = "/api/tweets/{0}/likes"
