"""
This module provides a class, for modifying the OpenAPI schema.

CustomOpenAPI includes functionality to specify certain routes
for which the default schema should be altered.
This is particularly useful when you want the OpenAPI documentation
to be different from the actual route behavior.

The class also has a method to generate the finalized OpenAPI schema,
reflecting these customizations.

Classes:
--------
- CustomOpenAPI: Enables customization of the OpenAPI schema.
    In particular, it allows you to mark routes for modification
    and generate the final schema.

Modules:
--------
- fastapi: Web framework for building APIs.
- get_openapi from fastapi.openapi.utils: A FastAPI utility for
    generating the OpenAPI schema.
- typing: the module to provide type information for methods
    and enhances the readability and debugging of the code.
"""

from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


class CustomOpenAPI:
    """
    A class to customize the OpenAPI schema for FastAPI app.

    This class allows users to modify OpenAPI schemas for specific
    routes defined in the field "routes_to_modify".

    Fields:
    -------
        routes_to_modify (List[str]):
            Routes which need their OpenAPI schemas to be modified.
    """

    routes_to_modify: List[str] = ["/api/tweets", "/api/users/me"]

    @classmethod
    def add_route_for_modification(cls, route: str) -> None:
        """
        Add a specific route to be modified in the OpenAPI schema.

        This class method takes a route and appends it to the class variable
        routes_to_modify which will later be used in customizing the OpenAPI
        schema.

        Args:
            route (str):
                The route to be added in the routes_to_modify list.
        """
        cls.routes_to_modify.append(route)

    @classmethod
    def take_custom_schema(
        cls,
        status_code_for_deletion: str,
    ) -> Dict[str, Any]:
        """
        Generate or retrieve a custom OpenAPI schema for the application.

        If an OpenAPI schema already exists for the app, it is returned.
        Otherwise, a new schema is created: an original OpenAPI schema is
        retrieved using 'get_openapi' method and then modified using
        'create_custom_schema' method to generate a custom schema.

        The created custom schema is stored to the app and also returned.

        Args:
            status_code_for_deletion (str):
                The response status code that needs to be removed
                from 'GET' methods responses of specific paths in the schema.

          Returns:
              Dict[str, Any]: The existing or newly created custom OpenAPI
              schema for the app.
        """
        from application.main import app

        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema: Dict[str, Any] = cls.get_openapi(application=app)
        custom_openapi_schema: Dict[str, Any] = cls.create_custom_schema(
            open_api_schema=openapi_schema,
            status_code_for_deletion=status_code_for_deletion,
        )
        app.openapi_schema = custom_openapi_schema
        return app.openapi_schema

    @classmethod
    def create_custom_schema(
        cls,
        open_api_schema: Dict[str, Any],
        status_code_for_deletion: str,
    ) -> Dict[str, Any]:
        """
        Generate a custom OpenAPI schema by modifying the provided schema.

        Iterates through each path in the provided OpenAPI schema and makes
        modifications to the methods of each path with the help of the
        'modify_methods' class method.

        Specifically, it removes the optional 'testing' parameter from the
        method, it also removes the specified response status code from the
        'GET' methods' responses for paths listed in 'cls.routes_to_modify'.

        Args:
            open_api_schema (Dict[str, Any]):
                The original OpenAPI schema to modify.
            status_code_for_deletion (str):
                The response status code that needs to be removed
                from 'GET' methods' responses for specific paths.

          Returns:
              Dict[str, Any]: The modified OpenAPI schema.
        """
        for path, path_dict in open_api_schema["paths"].items():
            open_api_schema["paths"][path] = cls.modify_methods(
                path_dict=path_dict,
                path=path,
                status_code_for_deletion=status_code_for_deletion,
            )

        return open_api_schema

    @classmethod
    def modify_methods(
        cls,
        path_dict: Dict[str, Any],
        path: str,
        status_code_for_deletion: str,
    ) -> Dict[str, Any]:
        """
        Modify the methods of a given path in an OpenAPI schema.

        For each method in the path dictionary, it deletes the optional
        parameter 'testing' from the method using
        'delete_optional_parameter_from_method' and updates the method's
        parameters.

        For specified paths (defined in 'cls.routes_to_modify'), if the
        method is a 'GET' method and it has a response status code that
        needs to be deleted, the status code is removed from method's
        responses.

        Args:
            path_dict (Dict[str, Any]):
                A dictionary representing the details of all methods in a path.
            path (str):
                The path whose methods should be modified.
            status_code_for_deletion (str):
                The status code to be removed from 'GET'
                methods responses of specified paths.

        Returns:
            Dict[str, Any]: The modified path dictionary with updated methods.
        """
        for method, method_dict in path_dict.items():
            open_api_parameters: List[Dict[str, Any]] = (
                cls.delete_optional_parameter_from_method(
                    method_dict=method_dict,
                )
            )
            method_dict["parameters"] = open_api_parameters

            if path in cls.routes_to_modify:
                if cls.has_method_get_with_code_to_delete(
                    status_code_for_deletion=status_code_for_deletion,
                    method=method,
                    method_dict=method_dict,
                ):
                    method_dict["responses"].pop(
                        status_code_for_deletion,
                        None,
                    )

        return path_dict

    @classmethod
    def get_openapi(cls, application: FastAPI):
        """
        Generate and return the OpenAPI schema for the FastAPI app.

        This method is designed to generate and return the OpenAPI schema,
        which is a standardized and language-agnostic description of your API.
        The function from fastapi.openapi.utils is being used to generate the
        schema.

        The schema includes details such as the title, version, and description
        of your API, as well as detailing the available API routes.

        Args:
            application (FastAPI):
                current application

        Returns:
            A dictionary containing the OpenAPI schema.
        """
        return get_openapi(
            title="Twitter clone",
            version="2.5.0",
            description="""Our Twitter clone is a social platform that
            offers users instant connection and real-time exchange of
            thoughts, news, and information. Create messages up to 280
            characters long, share your thoughts, ideas, photos, and
            videos with millions of people worldwide. Follow interesting
            people, topics, and events, participate in discussions, like,
            repost, and comment. Our Twitter clone is a place where everyone
            can find their audience, express themselves, and stay updated
            on the latest events.""",
            routes=application.routes,
        )

    @classmethod
    def delete_optional_parameter_from_method(
        cls,
        method_dict: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Delete an optional parameter from the specified method.

        This class method takes a dictionary representing a method and
        filters out the optional 'testing' parameter from the 'parameters'
        list in the dictionary.

        Args:
            method_dict (Dict[str, Any]):
                The dictionary representing a method from which the 'testing'
                parameter needs to be removed.

           Returns:
               A list of dictionaries representing the method parameters after
               removal of the 'testing' parameter.
        """
        return list(
            filter(
                lambda parameter: parameter.get("name") != "testing",
                method_dict["parameters"],
            ),
        )

    @classmethod
    def has_method_get_with_code_to_delete(
        cls,
        method: str,
        method_dict: Dict[str, Any],
        status_code_for_deletion: str,
    ) -> bool:
        """
        Check if a 'GET' method has a status code that needs to be removed.

        This method checks if the given method is a 'GET' method and
        if the response status code that needs to be deleted is
        in the response of the method dictionary.

        Args:
            method (str):
                The method type to check.
            method_dict (Dict[str, Any]):
                A dictionary representing details about the method.
            status_code_for_deletion (str):
                The response status code that needs to be checked
                for deletion from the method's responses.

        Returns:
            bool: True if the method is 'GET' and the status code for
            deletion is in the method's responses, False otherwise.
        """
        return (
            method.upper() == "GET"
            and status_code_for_deletion in method_dict.get("responses", {})
        )
