"""
This module defines a custom exception class for media ID validation.

The module provides a `MediaIdValidationError` class that inherits
from Python's built-in `Exception` class to handle cases where a
provided media ID is not valid.

Classes:
--------
MediaIdValidationError:
    Exception raised when the provided media ID is not valid.

Exception:
    Base class for all exceptions.
    Provides the base for user-defined exceptions.
"""


class MediaIdValidationError(Exception):
    """A custom exception class for handling media ID validation errors."""

    def __init__(self, message="Invalid media ID"):
        """
        Construct the `MediaIdValidationError` class.

        Args:
            message (str, optional): Custom error message to describe the
                                        media ID validation error.
                                        If not provided, the default message
                                        is "Invalid media ID."
        """
        self.message = message
        super().__init__(self.message)
