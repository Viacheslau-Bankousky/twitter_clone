"""
A module representing a basic pydantic models.

These models are used for formulating success responses in a consistent
way across the application.

Classes:
--------
BasicSuccessResponse:
    Represents a basic success response with only one field 'result'
    which indicates success.

ExtendedSuccessResponse:
    Represents an extended success response which includes 'id'.
    Inherits from BasicSuccessResponse.

Modules:
--------
pydantic: A data validation and settings management library using
python type annotations.

"""

from pydantic import BaseModel, Field


class BasicSuccessResponse(BaseModel):
    """
    Represents a Basic Success Response in the application.

    Fields:
    -------
    result (bool):
        Indicates whether the operation was successful.
        The default is 'True'.
    """

    result: bool = Field(default=True, description="Success")  # noqa: WPS110


class ExtendedSuccessResponse(BasicSuccessResponse):
    """
    Represents an Extended Success Response.

    This model inherits from BasicSuccessResponse and adds
    another field to the model.

    Fields:
    -------
    id (int):
        ID of added user instance.
    """

    id: int = Field(..., description="ID of added user instance")
