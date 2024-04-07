"""
This module defines a custom exception class for self-unfollowing validation.

The module provides a `SelfUnFollowingValidationError` class that inherits
from Python's built-in `Exception` class to handle cases where a user
tries to unsubscribe from their own content or unfollow themselves.

Classes:
--------
SelfUnFollowingValidationError:
    Exception raised when a user tries to unsubscribe or unfollow themselves.

Exception:
    Base class for all exceptions.
    Provides the base for user-defined exceptions.
"""


class SelfUnFollowingValidationError(Exception):
    """A custom exception for handling self-unfollowing validation errors."""

    def __init__(self, message="Trying to unsubscribe to yourself"):
        """
        Construct the `SelfUnFollowingValidationError` class.

        Args:
            message (str, optional): Custom error message to describe the
                                        self-unfollowing validation error.
                                        If not provided, the default message
                                        is "Trying to unsubscribe to yourself."
        """
        self.message = message
        super().__init__(self.message)
