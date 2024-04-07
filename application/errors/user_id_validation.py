"""
This module defines a custom exception class for user ID validation.

The module provides a `UserIdValidationError` class that inherits
from Python's built-in `Exception` class.
The exception is raised in cases where a provided user ID is not valid.

Classes:
--------
UserIdValidationError:
    Exception raised when the provided user ID is not valid.

Exception:
    Base class for all exceptions.
    Provides the base for user-defined exceptions.
"""


class UserIdValidationError(Exception):
    """A custom exception for handling user ID validation errors."""

    def __init__(self, message="Invalid user ID"):
        """
        Construct the `UserIdValidationError` class.

        Args:
            message (str, optional): Custom error message to describe the
                                    user ID validation error.
                                    If not provided, the default message
                                    is "Invalid user ID."
        """
        self.message = message
        super().__init__(self.message)
