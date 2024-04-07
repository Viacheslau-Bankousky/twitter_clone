"""
This module handles the API routes for Tweet and User related operations.

Routes include getting all current user's tweets, retrieving data
about the current user, and getting information about a specific user by ID.

Functions:
----------
get_tweets:
    Route for getting all of the current user's tweets.
get_current_user:
    Route for retrieving current user's data.
get_user:
    Route for getting a user's information based on the user_id.

Modules:
--------
typing: Provides type hints compatibility.
fastapi: Provides a highly efficient and easy to use platform for building
APIs.
application.logger.logger_instance: Manages logging instances across the
application.
application.main: Holds core components like api_key_header, app etc. required
across the application.
application.models.tweet: Contains methods and fields for the 'Tweet' entity.
application.models.user: Houses methods and fields for the 'User' entity.
application.schemas.error_schemas: Includes error response schemas for the
API.
application.schemas.tweet_schemas: Includes response schemas for tweet
operations.
application.schemas.user_schemas: Includes response schemas for user
operations.

"""

from typing import Annotated, List, Optional

from fastapi import Depends, Path, Request, status

from application.logger.logger_instance import app_logger
from application.main import MAIN_DEPENDENCY, api_key_header, app
from application.models.user import User
from application.schemas.error_schemas import GenericError
from application.schemas.tweet_schemas import AllTweetsResponse
from application.schemas.tweet_schemas import Tweet as TweetSchema
from application.schemas.user_schemas import UserResponse

MODEL_KEY: str = "model"


@app.get(
    "/api/tweets",
    description="A list of all the current user's tweets",
    status_code=status.HTTP_200_OK,
    response_description="A list of all the current user's tweets",
    responses={
        status.HTTP_200_OK: {MODEL_KEY: AllTweetsResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {MODEL_KEY: GenericError},
    },
    dependencies=[Depends(api_key_header)],
)
async def get_tweets(
    session_manager: MAIN_DEPENDENCY,
    request: Request,
):
    """
    Get all tweets from the current user's account.

    Args:
        session_manager (MAIN_DEPENDENCY):
            DB session manager to perform database transactions.
        request (Request):
            Original HTTP request sent by the client.

    Returns:
        AllTweetsResponse: A list of all tweets from the current
        users account.
    """
    app_logger.info("Getting tweets")
    async with session_manager as session:
        tweets: Optional[List[TweetSchema]] = await User.get_all_tweets(
            session=session,
            user=request.state.user,
        )
    return AllTweetsResponse(tweets=tweets)


@app.get(
    "/api/users/me",
    description="Get user information",
    status_code=status.HTTP_200_OK,
    response_description="The user information",
    responses={
        status.HTTP_200_OK: {MODEL_KEY: UserResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {MODEL_KEY: GenericError},
    },
    dependencies=[Depends(api_key_header)],
)
async def get_current_user(
    session_manager: MAIN_DEPENDENCY,
    request: Request,
):
    """
    Get information about the current user.

    Args:
        session_manager (MAIN_DEPENDENCY):
            DB session manager to perform database transactions.
        request (Request):
            Original HTTP request sent by the client.

    Returns:
        User: User instance representing the current user.
    """
    app_logger.info("Getting current user data")
    async with session_manager as session:
        user: Optional[UserResponse] = (
            await User.get_actual_data_of_current_user(
                session=session,
                user=request.state.user,
            )
        )
    return user


@app.get(
    "/api/users/{user_id}",
    description="Get information about the selected user",
    status_code=status.HTTP_200_OK,
    response_description="The selected user information",
    responses={
        status.HTTP_200_OK: {MODEL_KEY: UserResponse},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {MODEL_KEY: GenericError},
        status.HTTP_400_BAD_REQUEST: {MODEL_KEY: GenericError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {MODEL_KEY: GenericError},
    },
    dependencies=[Depends(api_key_header)],
)
async def get_user(
    user_id: Annotated[int, Path(description="user's ID", gt=0)],
    session_manager: MAIN_DEPENDENCY,
):
    """
    Get information about a particular user identified by the provided ID.

    Args:
        user_id (int):
            ID of the user to get information about.
        session_manager (MAIN_DEPENDENCY):
            DB session manager to perform database transactions.

    Returns:
        User: User instance representing the user with the provided ID.
    """
    app_logger.info("Getting user data by ID")
    async with session_manager as session:
        user: Optional[UserResponse] = (
            await User.get_actual_data_of_user_by_id(
                session=session,
                user_id=user_id,
            )
        )
    return user
