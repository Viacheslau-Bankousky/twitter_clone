"""
This module defines a custom exception class for image validation.

The module provides an `ImageValidationError` class that inherits
from Python's built-in `Exception` class to handle cases where an
uploaded file is not a valid image.

Classes:
--------
ImageValidationError:
    Exception raised when an uploaded file is not a valid image.

Exception:
    Base class for all exceptions.
    Provides the base for user-defined exceptions.
"""


class ImageValidationError(Exception):
    """A custom exception class for handling image validation errors."""

    def __init__(self, message="Uploaded file is not a valid image."):
        """
        Construct the `ImageValidationError` class.

         Args:
            message (str, optional): Custom error message to describe the
                                     image validation error.
                                     If not provided, the default message
                                     is "Uploaded file is not a valid image."
        """
        self.message = message
        super().__init__(self.message)
