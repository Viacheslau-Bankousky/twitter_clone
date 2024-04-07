"""
This module defines a custom exception class for Tweet ID validation.

The module provides a `TweetIdValidationError` class that inherits
from Python's built-in `Exception` class to handle cases where a
provided Tweet ID is not valid.

Classes:
--------
TweetIdValidationError:
    Exception raised when the provided Tweet ID is not valid.

Exception:
    Base class for all exceptions.
    Provides the base for user-defined exceptions.
"""


class TweetIdValidationError(Exception):
    """A custom exception for handling Tweet ID validation errors."""

    def __init__(self, message="Invalid tweet ID"):
        """
        Construct the `TweetIdValidationError` class.

        Args:
            message (str, optional): Custom error message to describe the
                                    Tweet ID validation error.
                                    If not provided, the default message
                                    is "Invalid tweet ID."
        """
        self.message = message
        super().__init__(self.message)
