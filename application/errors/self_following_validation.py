"""
This module defines a custom exception class for self-following validation.

The module provides a `SelfFollowingValidationError` class that inherits
from Python's built-in `Exception` class to handle cases where a user
tries to subscribe to their own content or follow themselves.

Classes:
--------
SelfFollowingValidationError:
    Exception raised when a user tries to subscribe or follow themselves.

Exception:
    Base class for all exceptions.
    Provides the base for user-defined exceptions.
"""


class SelfFollowingValidationError(Exception):
    """A custom exception for handling self-following validation errors."""

    def __init__(self, message="Trying to subscribe to yourself"):
        """
        Construct the `SelfFollowingValidationError` class.

        Args:
            message (str, optional): Custom error message to describe the
                                             self-following validation error.
                                             If not provided, the default
                                             message is "Trying to subscribe
                                             to yourself."
        """
        self.message = message
        super().__init__(self.message)
