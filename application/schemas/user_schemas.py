"""
A Pydantic module that contains models for managing user-related interactions.

These models help in constructing standardized requests and responses
within the user-related features in the application.

Classes:
--------
UserConnections:
    A model defining the connections for a User.

User:
    A model defining detailed information of a User, including the users
    they're following or being followed by.

UserResponse:
    A model defining the response structure including User information.

UserRequest:
    A model defining the request structure for creating or updating a User.

Modules:
--------
typing: Supports type hints.
pydantic: A data validation and settings management library using Python
type annotations.
application.schemas.basic_schemas: Contains basic response schemas.
"""

from typing import List

from pydantic import BaseModel, Field

from application.schemas.basic_schemas import BasicSuccessResponse


class UserConnections(BaseModel):
    """
    Represents User's connections in the application.

    Fields:
    -------
    id (int):
        Unique identifier for the connected user.
    name (str):
        Name of the connected user.
    """

    id: int = Field(..., description="User ID")
    name: str = Field(..., description="User name")


class User(BaseModel):
    """
    Represents a User including followers and followed.

    Fields:
    -------
    id (int):
        Unique identifier for the User.
    name (str):
        Name of the User.
    followers (List[UserConnections]):
        List of users following this User.
    following (List[UserConnections]):
        List of users this User is following.
    """

    id: int = Field(..., description="User ID")
    name: str = Field(..., description="User name")
    followers: List[UserConnections] = Field(
        ..., description="List of user followers",
    )
    following: List[UserConnections] = Field(
        ..., description="List of users being followed",
    )


class UserResponse(BasicSuccessResponse):
    """
    The response model for retrieving users.

    Inherits from BasicSuccessResponse and adds the user details.

    Fields:
    -------
    user (User):
        Detailed information of the retrieved User.
    """

    user: User = Field(..., description="User info")


class UserRequest(BaseModel):
    """
    The request model for creating or updating a User.

    Fields:
    -------
    name (str):
        Name of the User.
    api_key (str):
        API key for the User.
    """

    name: str = Field(..., description="User name")
    api_key: str = Field(..., alias="api-key", description="API key")
