"""
This module contains FastAPI middlewares for the application.

Middlewares are used for processing that needs to be made on
requests or responses, before passing them to any incoming
request or before sending any outgoing responses.

Modules:
--------
fastapi: Web framework for building APIs.
typing: Support for type hints.

Functions:
----------
api_key_middleware() -> Response:
    Middleware used for authenticating requests with the API key.

exception_middleware(request: Request, call_next: Callable[[Request],
    Awaitable[Response]]) -> Response:
    Middleware used for handling errors and exceptions.
"""

from typing import Awaitable, Callable

from fastapi import Request, Response

from application.logger.logger_instance import app_logger
from application.main import app
from application.middlewares.api_key_authentication import check_api_key
from application.middlewares.exception_middleware import ErrorHandler


@app.middleware("http")
async def api_key_middleware(*args, **kwargs) -> Response:
    """
    Authenticate requests with the API key.

    This function checks if the API key in the request is valid.

    Args:
        args:
            Variable length argument list.
        kwargs:
            Arbitrary keyword arguments.

    Returns:
        Response: The response of the request if the API key is valid,
        raises an exception otherwise.
    """
    app_logger.info("Running API key check middleware")
    return await check_api_key(*args, **kwargs)


@app.middleware("http")
async def exception_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """
    Handle errors and exceptions.

    This function handles exceptions that occur during the handling
    of a request.
    It is used either to return a response with a specific status
    code or optionally to re-raise exceptions.

    Args:
        request (Request):
            The incoming request.
        call_next (Callable):
            The function to be called next.

    Returns:
        Response: The response of the request if no exception was caught,
        returns an error response otherwise.
    """
    app_logger.info("Running errors handling middleware")
    return await ErrorHandler.handle_errors(request, call_next)
