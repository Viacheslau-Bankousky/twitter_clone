"""
Sets up the testing application with required routes and middleware.

Provides `test_app`, an instance of `CustomFastAPI` with all the
required routes and middleware included for testing.
Uses the `CustomFastAPI` framework and the specific middleware and
routes from the `application` package.

Modules:
--------
typing: For Callable type annotation
fastapi: The web framework being used
fastapi.exceptions: For handling exceptions within the framework
application.api_utils.custom_fast_api: Provides an extension of
FastAPI for customization
application.middlewares.api_key_authentication: Middleware for
checking API key
application.middlewares.exception_middleware: Middleware for
handling exceptions
application.routes.delete_routes: Routes for delete requests
application.routes.error_handler: Error handler for routes
application.routes.get_routes: Routes for get requests
application.routes.post_routes: Routes for post requests
tests.app_for_testing.lifespan.lifespan: Lifespan events for
the application

"""
from typing import Callable

from fastapi import Request, Response, status
from fastapi.exceptions import RequestValidationError

from application.api_utils.custom_fast_api import CustomFastAPI
from application.middlewares.api_key_authentication import check_api_key
from application.middlewares.exception_middleware import ErrorHandler
from application.routes.delete_routes import (
    delete_tweet,
    unfollow_user,
    unlike_tweet,
)
from application.routes.error_handler import validation_exception_handler
from application.routes.get_routes import (
    get_current_user,
    get_tweets,
    get_user,
)
from application.routes.post_routes import (
    create_media,
    create_tweet,
    create_user,
    follow_user,
    like_tweet,
)

MODEL_KEY: str = "model"

test_app = CustomFastAPI()
test_app.add_exception_handler(
    exc_class_or_status_code=RequestValidationError,
    handler=validation_exception_handler,  # type: ignore
)
test_app.add_api_route(
    endpoint=create_user,
    path="/api/users/new",
    methods=["POST"],
    status_code=status.HTTP_201_CREATED,
)
test_app.add_api_route(
    endpoint=create_tweet,
    path="/api/tweets",
    methods=["POST"],
    status_code=status.HTTP_201_CREATED,
)
test_app.add_api_route(
    endpoint=get_tweets,
    path="/api/tweets",
    methods=["GET"],
    status_code=status.HTTP_200_OK,
)
test_app.add_api_route(
    endpoint=create_media,
    path="/api/medias",
    methods=["POST"],
    status_code=status.HTTP_201_CREATED,
)
test_app.add_api_route(
    endpoint=like_tweet,
    path="/api/tweets/{tweet_id}/likes",
    methods=["POST"],
    status_code=status.HTTP_201_CREATED,
)
test_app.add_api_route(
    endpoint=follow_user,
    path="/api/users/{user_id}/follow",
    status_code=status.HTTP_201_CREATED,
    methods=["POST"],
)
test_app.add_api_route(
    endpoint=get_current_user,
    path="/api/users/me",
    methods=["GET"],
    status_code=status.HTTP_200_OK,
)
test_app.add_api_route(
    endpoint=get_user,
    path="/api/users/{user_id}",
    status_code=status.HTTP_200_OK,
    methods=["GET"],
)
test_app.add_api_route(
    endpoint=delete_tweet,
    path="/api/tweets/{tweet_id}",
    status_code=status.HTTP_200_OK,
    methods=["DELETE"],
)
test_app.add_api_route(
    endpoint=unlike_tweet,
    path="/api/tweets/{tweet_id}/likes",
    status_code=status.HTTP_200_OK,
    methods=["DELETE"],
)
test_app.add_api_route(
    endpoint=unfollow_user,
    path="/api/users/{user_id}/follow",
    status_code=status.HTTP_200_OK,
    methods=["DELETE"],
)


@test_app.middleware("http")
async def test_middleware_for_checking_api_key(
    request: Request, call_next: Callable,
) -> Response:
    """
    Check the API key for each request during testing.

    This is added as a middleware to the FastAPI app.

    Args:
        request (Request):
            Contains info about incoming request.
        call_next (Callable):
            The next middleware function to be called.

    Returns:
        The response generated after processing the request.
    """
    return await check_api_key(request, call_next)


@test_app.middleware("http")
async def test_middleware_for_checking_errors(
    request: Request, call_next: Callable,
) -> Response:
    """
    Handle errors for each request during testing.

    This is added as a middleware to the FastAPI app.

    Args:
        request (Request):
            Contains info about incoming request.
        call_next (Callable):
            The next middleware function to be called.

    Returns:
        The response generated after processing the request.
    """
    return await ErrorHandler.handle_errors(request, call_next)
