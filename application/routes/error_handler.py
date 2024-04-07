"""
This module handles validation errors in the FastAPI application.

If a request does not pass validation checks, an error is logged and a response
with HTTP status code 400 (Bad Request) is returned to the client with a clear
error message indicating the problem.

This is part of the error handling and logging infrastructure of the
application, contributing to its robustness and maintainability.

It makes use of FastAPI's application decorator for exception handling.

Handlers:
---------
validation_exception_handler(Request, RequestValidationError) -> JSONResponse:
    Handles invalid request exceptions by logging the error and responding
    with a 400 status code.

Modules:
--------
fastapi: The web framework for building APIs with Python 3.7+ based on
standard Python type hints.
fastapi.exceptions: Exceptions module for FastAPI library.
fastapi.responses: Allows to send various response types with FastAPI,
such as JSONResponse.

"""

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from application.api_utils.generate_error_response import (
    generate_error_response,
)
from application.logger.logger_instance import app_logger
from application.main import app


@app.exception_handler(RequestValidationError)
def validation_exception_handler(
    _request: Request,
    _exc: RequestValidationError,
) -> JSONResponse:
    """
    Handle exceptions for invalid requests.

    This method responds to invalid requests by sending a JSON response
    with a status code 400 (Bad Request) and an error message.

    Args:
        _request (Request): The request that caused the exception.
        _exc (RequestValidationError): The exception (validation error) itself.

    Returns:
        JSONResponse: The response in JSON format containing result as
                        `False`, with error type and error message.
    """
    app_logger.exception("Request validation error: {0}".format(_exc))
    return generate_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_type="Request Validation Error",
        error_message="""Invalid input was sent.
        Please review the API documentation
        for correct input formats.""",
    )
