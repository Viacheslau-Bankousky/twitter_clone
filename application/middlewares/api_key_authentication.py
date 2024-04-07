"""
This module encompasses the middleware logic for API key authentication.

It carries an asynchronous function 'check_api_key', which checks the
validity of the provided API key in the header of the incoming requests.
It matches the API key with the existing users' keys in the database to
authenticate the requests.

Modules:
--------
typing: Provides all the type hints needed in the function.
fastapi: Framework used for building APIs.
application.api_utils.user_data_processing: Contains utilities for processing
user data.
application.database.connection: Handles database connection related tasks.
application.logger.logger_instance: Logs the application tasks.
application.models.user: Module including the User model.

Functions:
----------
async def check_api_key(request: Request, call_next: Callable[[Request],
 Awaitable[Response]]) -> Response:
    Authenticates the user by checking if the provided API key matches
     with existing users' keys.
"""

from typing import Awaitable, Callable, Optional

from fastapi import HTTPException, Request, Response, status

from application.api_utils.user_data_processing import hash_api_key
from application.database.connection import get_session
from application.logger.logger_instance import app_logger
from application.models.user import User


async def check_api_key(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Check validity of user's API key.

    It checks all incoming HTTP requests, except for the endpoints
    "/api/users/new", "/docs" and "/openapi.json".
    If the api-key is valid, the user will be got from a database and passed
    to the endpoint

    Args:
        request (Request): FastAPI request object, encapsulates the incoming
            HTTP request.
        call_next (Callable): A callable that will be used to process the
            request and generate the response within the middleware stack.

    Returns:
        Response: The response generated by processing the request.

    Raises:
        HTTPException: If `api-key` header is not included in the request
            or if the provided API key does not match an existing user's API
            key in the database.
    """
    app_logger.info("Checking API Key")
    api_key: Optional[str] = request.headers.get("api-key")
    path: str = request.url.path
    if path == "/api/users/new" or path in {"/openapi.json", "/docs"}:
        app_logger.info(
            "API Key will not be used (adding a new user or read API doc)",
        )
        return await call_next(request)
    if api_key is None:
        app_logger.exception("No API key provided")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="api-key header required",
        )
    encrypted_api_key: str = hash_api_key(api_key=api_key)
    app_logger.info("Searching for existing user with API key")
    async with get_session() as session:
        user: Optional["User"] = await User.get_user_by_api_key(
            session=session,
            api_key=encrypted_api_key,
        )
    if user is None:
        app_logger.exception("Invalid API key")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid api-key header",
        )
    app_logger.info("User with API key found")
    request.state.user = user
    app_logger.info("API key successfully checked")
    return await call_next(request)
