"""
This module manages the application's exception handling.

The `ErrorHandler` class catches various types of exceptions, providing an
appropriate response for each.
It handles the exceptions that could occur during the handling of a request,
and provides an error response corresponding to the type of exception that
occurred.

Modules:
--------
typing: Provides type hints including complex types such as Union,
Callable, etc.
fastapi: Starlette-based framework for building web applications.
sqlalchemy: SQL toolkit and Object-Relational Mapping (ORM) system.
application.api_utils.generate_error_response: Contains the function
for generating the error response.
All the imported modules from application.errors: Provide custom error
classes for validation.
application.logger.logger_instance: Handles the logging
in the application.

Classes:
--------
ErrorHandler:
    Class that centralizes the handling of exceptions occurring during
    the processing of requests.
"""

from typing import Awaitable, Callable, Dict, NewType, Optional, Type, Union

from fastapi import Request, Response, status
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm.exc import UnmappedInstanceError

from application.api_utils.generate_error_response import (
    generate_error_response,
)
from application.errors.image_validation import ImageValidationError
from application.errors.media_id_validation import MediaIdValidationError
from application.errors.self_following_validation import (
    SelfFollowingValidationError,
)
from application.errors.self_unfollowing_validation import (
    SelfUnFollowingValidationError,
)
from application.errors.tweet_id_validation import TweetIdValidationError
from application.errors.user_id_validation import UserIdValidationError
from application.logger.logger_instance import app_logger

BAD_REQUEST_STATUS_CODE: int = status.HTTP_400_BAD_REQUEST
STATUS_CODE: str = "status_code"
ERROR_MESSAGE: str = "error_message"
ERROR_TYPE: str = "error_type"

common_error_message: Dict[str, Union[int, str]] = {
    STATUS_CODE: BAD_REQUEST_STATUS_CODE,
    ERROR_MESSAGE: "The provided id could not be found",
    ERROR_TYPE: "IDValidationError",
}

error_content = NewType("error_content", Dict[str, Union[int, str]])
error_handler_mapping = NewType(
    "error_handler_mapping",
    Dict[Type[Exception], error_content],
)


class ErrorHandler:
    """The ErrorHandler class centralizes the logic for handling exceptions.

    It maps each kind of exception to a dict containing information that
    should be included in the response to the client when that exception
    occurs.
    """

    error_handlers: error_handler_mapping = {  # type: ignore
        ImageValidationError: {
            STATUS_CODE: BAD_REQUEST_STATUS_CODE,
            ERROR_MESSAGE: "Failed attempt to upload a photo",
            ERROR_TYPE: "ImageValidationError",
        },
        IntegrityError: {
            STATUS_CODE: BAD_REQUEST_STATUS_CODE,
            ERROR_MESSAGE: "the transferred data is already exists",
            ERROR_TYPE: "UniqueDataError",
        },
        UnmappedInstanceError: {
            STATUS_CODE: BAD_REQUEST_STATUS_CODE,
            ERROR_MESSAGE: "Nothing to delete",
            ERROR_TYPE: "UnmappedInstanceError",
        },
        SelfFollowingValidationError: {
            STATUS_CODE: BAD_REQUEST_STATUS_CODE,
            ERROR_MESSAGE: "It is impossible to subscribe to yourself",
            ERROR_TYPE: "SelfFollowingValidationError",
        },
        SelfUnFollowingValidationError: {
            STATUS_CODE: BAD_REQUEST_STATUS_CODE,
            ERROR_MESSAGE: "It is impossible to unsubscribe to yourself",
            ERROR_TYPE: "SelfUnFollowingValidationError",
        },
        UserIdValidationError: common_error_message,
        TweetIdValidationError: common_error_message,
        InvalidRequestError: common_error_message,
        MediaIdValidationError: common_error_message,
    }

    @classmethod
    async def handle_errors(
        cls,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Handle a FastAPI request and catch any exceptions that occur.

        Args:
            request (Request):
                The incoming HTTP request.
            call_next (Callable):
                A callable that will process the request and generate the
                response.

        Returns:
            The HTTP response generated by the callable 'call_next' or an error
            response if an exception occurs.
        """
        try:
            return await call_next(request)
        except Exception as exc:
            error_info: Optional[error_content] = cls.error_handlers.get(
                type(exc),
            )
            app_logger.exception(
                "Error handling request: {0}".format(str(exc)),
            )
            if error_info:
                return generate_error_response(
                    status_code=int(error_info[STATUS_CODE]),
                    error_type=str(error_info[ERROR_TYPE]),
                    error_message=str(error_info[ERROR_MESSAGE]),
                )
            return generate_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_type=str(type(exc).__name__),
                error_message="Something went wrong on the server side",
            )

    @classmethod
    async def add_error(
        cls,
        exception: Type[Exception],
        exception_description: error_content,
    ) -> None:
        """Add additional exception mapping to dict with exception info.

        Args:
            exception (Type[Exception]):
                The type of the exception.
            exception_description (error_content):
                Content dict associated with the exception.
        """
        cls.error_handlers.update({exception: exception_description})
