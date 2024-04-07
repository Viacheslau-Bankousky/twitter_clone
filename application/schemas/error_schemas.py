"""
A Pydantic module that represents the `GenericError` model.

This model is used for constructing uniform error responses
across the application.

Classes:
--------
GenericError:
    Represents a Generic Error Response in the application.

Modules:
--------
pydantic: A data validation and settings management library using
python type annotations.
"""

from pydantic import BaseModel


class GenericError(BaseModel):
    """
    Represents a Generic Error Response in the application.

    Fields:
    -------
    status_code (int):
        HTTP Status Code associated with the error.
    error_message (str):
        Detailed description of the error.
    error_type (str):
        Type or category of the error.
    """

    status_code: int
    error_message: str
    error_type: str
