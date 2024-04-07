"""
This module handles the API routes for Tweet and User related operations.

Routes include posting a new tweet, posting new media, liking a tweet,
following a user, and adding a new user.

Functions:
----------
create_tweet:
    Route for posting a new tweet.
create_media:
    Route for posting new media.
like_tweet:
    Route for liking a tweet.
follow_user:
    Route for following a user.
create_user:
    Route for adding a new user.

Modules:
--------
typing: Provides type hints compatibility.
fastapi: Provides a highly efficient and easy to use platform for building
APIs.
application.main: Holds core components like API key header, app etc.
required across the application.
application.models.tweet: Contains methods and fields for the 'Tweet'
entity.
application.models.user: Houses methods and fields for the 'User'
entity.
application.models.like: Provides model for 'Like' entity.
application.models.media: Provides model for 'Media' entity.
application.schemas.tweet_schemas: Includes response schemas for tweet
operations.
application.schemas.user_schemas: Includes response schemas for user
operations.
application.schemas.basic_schemas: Includes basic response schemas
for the API.
application.schemas.error_schemas: Includes error response schemas
for the API.
"""

from typing import Annotated, List, Optional

from fastapi import Depends, File, Path, Request, UploadFile, status

from application.api_utils.user_data_processing import (
    hash_api_key,
    shield_incoming_data,
)
from application.logger.logger_instance import app_logger
from application.main import MAIN_DEPENDENCY, api_key_header, app
from application.models.like import Like
from application.models.media import Media
from application.models.tweet import Tweet
from application.models.user import User
from application.schemas.basic_schemas import (
    BasicSuccessResponse,
    ExtendedSuccessResponse,
)
from application.schemas.error_schemas import GenericError
from application.schemas.tweet_schemas import (
    MediaResponse,
    TweetRequest,
    TweetResponse,
)
from application.schemas.user_schemas import UserRequest

MODEL_KEY: str = "model"


@app.post(
    "/api/tweets",
    description="Post a new tweet",
    status_code=status.HTTP_201_CREATED,
    response_description="The tweet posted",
    responses={
        status.HTTP_201_CREATED: {MODEL_KEY: TweetResponse},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {MODEL_KEY: GenericError},
        status.HTTP_400_BAD_REQUEST: {MODEL_KEY: GenericError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {MODEL_KEY: GenericError},
    },
    dependencies=[Depends(api_key_header)],
)
async def create_tweet(
    session_manager: MAIN_DEPENDENCY,
    tweet_request_data: TweetRequest,
    request: Request,
):
    """
    Post a new tweet.

    Args:
        session_manager (MAIN_DEPENDENCY):
            DB session manager to perform database transactions.
        tweet_request_data (TweetRequest):
            Object containing the data for creating the tweet.
        request (Request):
            Original HTTP request sent by the client.

    Returns:
        TweetResponse: Response object containing info about the
        newly created tweet.
    """
    app_logger.info(
        "Received request to create a new tweet: {0}".format(
            tweet_request_data,
        ),
    )
    tweet_data: str = shield_incoming_data(
        incoming_data=tweet_request_data.tweet_data,
    )
    tweet_media_ids: Optional[List[int]] = tweet_request_data.tweet_media_ids
    async with session_manager as session:
        new_tweet_id: Optional[int] = await Tweet.add_tweet(
            session=session,
            tweet_data=tweet_data,
            tweet_media_ids=tweet_media_ids,
            user=request.state.user,
        )
    app_logger.info(
        "Successfully created new tweet with ID: {0}".format(new_tweet_id),
    )
    if new_tweet_id:
        return TweetResponse(tweet_id=new_tweet_id)


@app.post(
    "/api/medias",
    description="Post a new media file",
    status_code=status.HTTP_201_CREATED,
    response_description="The media file posted",
    responses={
        status.HTTP_201_CREATED: {MODEL_KEY: MediaResponse},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {MODEL_KEY: GenericError},
        status.HTTP_400_BAD_REQUEST: {MODEL_KEY: GenericError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {MODEL_KEY: GenericError},
    },
    dependencies=[Depends(api_key_header)],
)
# fmt: off
async def create_media(
    session_manager: MAIN_DEPENDENCY,
    file: Annotated[UploadFile, File(description="The media file")],  # noqa: WPS110, E501
):
    # fmt: on
    """
    Post a new media file.

    Args:
        session_manager (MAIN_DEPENDENCY):
            DB session manager to perform database transactions.
        file (UploadFile):
            File being uploaded.

    Returns:
        MediaResponse: Response object containing info about the newly
        uploaded file.
    """
    app_logger.info("Received request to create a new media")
    async with session_manager as session:
        new_media_id: Optional[int] = await Media.add_media_to_database(
            session=session,
            media=file,
        )
    app_logger.info(
        "Successfully created new media with ID: {0}".format(new_media_id),
    )
    if new_media_id:
        return MediaResponse(media_id=new_media_id)


@app.post(
    "/api/tweets/{tweet_id}/likes",
    description="Likes a tweet",
    status_code=status.HTTP_201_CREATED,
    response_description="The tweet liked",
    responses={
        status.HTTP_201_CREATED: {MODEL_KEY: BasicSuccessResponse},
        status.HTTP_400_BAD_REQUEST: {MODEL_KEY: GenericError},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {MODEL_KEY: GenericError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {MODEL_KEY: GenericError},
    },
    dependencies=[Depends(api_key_header)],
)
async def like_tweet(
    tweet_id: Annotated[int, Path(description="tweet ID", gt=0)],
    session_manager: MAIN_DEPENDENCY,
    request: Request,
):
    """
    Like a tweet.

    Args:
        tweet_id (int):
            ID of the tweet being liked.
        session_manager (MAIN_DEPENDENCY):
            DB session manager to perform database transactions.
        request (Request):
            Original HTTP request sent by the client.

    Returns:
        BasicSuccessResponse: A basic response indicating the tweet
        has been liked.
    """
    app_logger.info("Received request to like a tweet")
    async with session_manager as session:
        await Like.add_like(
            session=session,
            tweet_id=tweet_id,
            user=request.state.user,
        )
    app_logger.info("Successfully liked a tweet")
    return BasicSuccessResponse()


@app.post(
    "/api/users/{user_id}/follow",
    description="Follow a user",
    status_code=status.HTTP_201_CREATED,
    response_description="Following the user",
    responses={
        status.HTTP_201_CREATED: {MODEL_KEY: BasicSuccessResponse},
        status.HTTP_400_BAD_REQUEST: {MODEL_KEY: GenericError},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {MODEL_KEY: GenericError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {MODEL_KEY: GenericError},
    },
    dependencies=[Depends(api_key_header)],
)
async def follow_user(
    user_id: Annotated[int, Path(description="user's ID", gt=0)],
    session_manager: MAIN_DEPENDENCY,
    request: Request,
):
    """
    Follows a user.

    Args:
        user_id (int):
            ID of the user being followed.
        session_manager (MAIN_DEPENDENCY):
            DB session manager to perform database transactions.
        request (Request):
            Original HTTP request sent by the client.

    Returns:
        BasicSuccessResponse: A basic response indicating the user
        has been followed.
    """
    app_logger.info("Received request to follow a user")
    async with session_manager as session:
        await User.follow_user(
            session=session,
            user_to_follow_id=user_id,
            current_user=request.state.user,
        )
    app_logger.info("Successfully followed the user")
    return BasicSuccessResponse()


@app.post(
    "/api/users/new",
    description="Add a new user",
    status_code=status.HTTP_201_CREATED,
    response_description="New user added",
    responses={
        status.HTTP_201_CREATED: {MODEL_KEY: ExtendedSuccessResponse},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {MODEL_KEY: GenericError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {MODEL_KEY: GenericError},
    },
)
async def create_user(
    session_manager: MAIN_DEPENDENCY,
    user_request_data: UserRequest,
):
    """
    Create a new user.

    Args:
        session_manager (MAIN_DEPENDENCY):
            DB session manager to perform database transactions.
        user_request_data (UserRequest):
            Object containing the data for creating the user.

    Returns:
        ExtendedSuccessResponse: A response object containing
        the new user's ID.
    """
    app_logger.info("Received request to create a new user")
    user_name: str = shield_incoming_data(incoming_data=user_request_data.name)
    encrypted_api_key: str = hash_api_key(api_key=user_request_data.api_key)
    async with session_manager as session:
        new_user_id: Optional[int] = await User.add_user(
            session=session,
            name=user_name,
            api_key=encrypted_api_key,
        )
    app_logger.info(
        "Successfully created new user with ID: {0}".format(new_user_id),
    )
    if new_user_id:
        return ExtendedSuccessResponse(id=new_user_id)
