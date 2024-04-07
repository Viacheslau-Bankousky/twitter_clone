"""
Module that contains the definition of a custom FastAPI application.

The `CustomFastAPI` class inherits from FastAPI but replaces
the OpenAPI method with a custom schema constructor that caters for
additional requirements around status code for deletion.

Class:
------
- CustomFastAPI: A specialized variant of the FastAPI application
  that constructs a customized OpenAPI schema.

Modules:
--------
- typing: Provides type hints compatibility.
- fastapi.FastAPI: The base FastAPI web application class.
- application.api_utils.custom_open_api.CustomOpenAPI: Contains
  definition for custom OpenAPI schema generation.
"""
from typing import Any, Dict

from fastapi import FastAPI

from application.api_utils.custom_open_api import CustomOpenAPI


class CustomFastAPI(FastAPI):
    """
    Implement CustomFastAPI Class.

    This class inherits the FastAPI class and replaces the
    default OpenAPI schema function with a custom one.

    It utilizes the custom schema construction method from
    `CustomOpenAPI` class to handle additional requirements
    specified by status codes for deletion.
    """

    def openapi(self) -> Dict[str, Any]:
        """
        Generate the OpenAPI schema for the application.

        This method checks if an OpenAPI schema is already defined,
        returning it if present. If no schema is defined, it creates
        a new schema using `CustomOpenAPI.take_custom_schema`.

        The status code for deletion provided for
        `CustomOpenAPI.take_custom_schema`
        is hardcoded as "422".

        Returns:
            dict: The existing or newly created OpenAPI schema.
        """
        if self.openapi_schema:
            return self.openapi_schema

        self.openapi_schema = CustomOpenAPI.take_custom_schema(
            status_code_for_deletion="422",
        )
        return self.openapi_schema
