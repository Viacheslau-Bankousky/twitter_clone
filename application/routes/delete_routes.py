"""
This module handles the API routes for Tweet and User related operations.

It includes routes for deleting a tweet, unliking a tweet, and unfollowing
a user.

Functions:
----------
delete_tweet:
    Handles the deletion of a particular tweet by its ID.
unlike_tweet:
    Handles the operation of a user unliking a tweet by its ID.
unfollow_user:
    Handles the operation of a user unfollowing another user by user's ID.

Modules:
--------
typing: Provides type hints compatibility.
fastapi: Provides a highly efficient and easy to use platform for building
APIs.
application.main: Contains the main dependencies for the application.
application.models.tweet: Contains methods and fields for the 'Tweet' entity.
application.models.user: Houses methods and fields for the 'User' entity.
application.models.like: Depicts 'Like' entity with its fields and methods.
application.schemas.basic_schemas: Includes basic response schemas for the API.
application.schemas.error_schemas: Includes error response schemas for the API.
application.logger.logger_instance: Controls logging in the application.

"""

from typing import Annotated

from fastapi import Depends, Path, Request, status

from application.logger.logger_instance import app_logger
from application.main import MAIN_DEPENDENCY, api_key_header, app
from application.models.like import Like
from application.models.tweet import Tweet
from application.models.user import User
from application.schemas.basic_schemas import BasicSuccessResponse
from application.schemas.error_schemas import GenericError

MODEL_KEY: str = "model"


@app.delete(
    "/api/tweets/{tweet_id}",
    description="Delete a tweet",
    status_code=status.HTTP_200_OK,
    response_description="The tweet deleted",
    responses={
        status.HTTP_200_OK: {MODEL_KEY: BasicSuccessResponse},
        status.HTTP_400_BAD_REQUEST: {MODEL_KEY: GenericError},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {MODEL_KEY: GenericError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {MODEL_KEY: GenericError},
    },
    dependencies=[Depends(api_key_header)],
)
async def delete_tweet(
    tweet_id: Annotated[int, Path(description="tweet ID", gt=0)],
    session_manager: MAIN_DEPENDENCY,
    request: Request,
):
    """
    Delete of a tweet of specified ID that belongs to a specified user.

    Args:
        tweet_id (Annotated[int, Path]):
            The ID of the tweet to be deleted.
        session_manager (MAIN_DEPENDENCY):
            The manager to handle all session-related tasks.
        request (Request):
            Request instance needed for having the user instance.

    Returns:
        BasicSuccessResponse: If the deletion is successful.
    """
    app_logger.info("Deleting tweet with ID: {0}".format(tweet_id))
    async with session_manager as session:
        await Tweet.delete_tweet(
            session=session, tweet_id=tweet_id, user=request.state.user,
        )
    app_logger.info("Successfully deleted tweet with ID: {0}".format(tweet_id))
    return BasicSuccessResponse()


@app.delete(
    "/api/tweets/{tweet_id}/likes",
    description="Unlikes a tweet",
    status_code=status.HTTP_200_OK,
    response_description="The tweet unliked",
    responses={
        status.HTTP_200_OK: {MODEL_KEY: BasicSuccessResponse},
        status.HTTP_400_BAD_REQUEST: {MODEL_KEY: GenericError},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {MODEL_KEY: GenericError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {MODEL_KEY: GenericError},
    },
    dependencies=[Depends(api_key_header)],
)
async def unlike_tweet(
    tweet_id: Annotated[int, Path(description="tweet ID", gt=0)],
    session_manager: MAIN_DEPENDENCY,
    request: Request,
):
    """
    Handle the operation of a user unliking a tweet of specified ID.

    Args:
        tweet_id (Annotated[int, Path]):
            The ID of the tweet to be unliked.
        session_manager (MAIN_DEPENDENCY):
            The manager to handle all session-related tasks.
        request (Request):
            The request instance provided by FastAPI.

    Returns:
        BasicSuccessResponse: If the unliking operation is successful.
    """
    app_logger.info("Unliked tweet with ID: {0}".format(tweet_id))
    async with session_manager as session:
        await Like.delete_like(
            session=session,
            tweet_id=tweet_id,
            user=request.state.user,
        )
    app_logger.info("Successfully unliked tweet with ID: {0}".format(tweet_id))
    return BasicSuccessResponse()


@app.delete(
    "/api/users/{user_id}/follow",
    description="Unfollow a user",
    status_code=status.HTTP_200_OK,
    response_description="Unfollowing the user",
    responses={
        status.HTTP_200_OK: {MODEL_KEY: BasicSuccessResponse},
        status.HTTP_400_BAD_REQUEST: {MODEL_KEY: GenericError},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {MODEL_KEY: GenericError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {MODEL_KEY: GenericError},
    },
    dependencies=[Depends(api_key_header)],
)
async def unfollow_user(
    session_manager: MAIN_DEPENDENCY,
    user_id: Annotated[int, Path(description="user's ID", gt=0)],
    request: Request,
):
    """
    Handle the operation of a user unfollowing another user of specified ID.

    Args:
        session_manager (MAIN_DEPENDENCY):
            The manager to handle all session-related tasks.
        user_id (Annotated[int, Path]):
            The ID of the user to be unfollowed.
        request (Request):
            The request instance provided by FastAPI.

    Returns:
        BasicSuccessResponse: If the unfollow operation is successful.
    """
    app_logger.info("Unfollowing user with ID: {0}".format(user_id))
    async with session_manager as session:
        await User.unfollow_user(
            session=session,
            user_to_unfollow_id=user_id,
            current_user=request.state.user,
        )
    app_logger.info(
        "Successfully unfollowed user with ID: {0}".format(user_id),
    )
    return BasicSuccessResponse()
