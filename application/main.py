"""
This module initializes the custom FastAPI application and configures it.

Notable configurations include setting up lifespan events, customizing API
documentation, as well as defining a primary AsyncSession context manager
instance to function as the main FastAPI dependency.

Modules:
--------
1) `typing.Annotated`, `typing.AsyncContextManager`: Used for type hinting.

2) `fastapi.Depends`: Functionality for dependency injection.

3) `sqlalchemy.ext.asyncio.AsyncSession`: Asynchronous SQLAlchemy ORM Session.

4) `application.database.connection.get_session`: Provides the asynchronous
SQLAlchemy session for the application.

5) `application.lifespan.app_lifespan.lifespan`: Contains lifespan events
for the application.

6) `application.api_utils.custom_fast_api.CustomFastAPI`: Customized FastAPI
class with an overridden openapi method.

7) `fastapi.security.api_key.APIKeyHeader`: Utility class for defining an API
Key header dependency.

Variables:
----------
1) `app`: Instance of the customized FastAPI application, `CustomFastAPI`.

2) `MAIN_DEPENDENCY`: Annotated FastAPI dependency which provides an Async
Context Manager with the AsyncSession for database interactions.

3) `api_key_header`: Instance of APIKeyHeader.
This is a FastAPI dependency that checks for a specific 'api-key' header
in the requests where it's applied.

Please note: The OpenAPI schema for FastAPI app is created and set when the
/docs endpoint is hit for the first time.
The OpenAPI schema is customized by overwriting the `openapi`
method of the initial FastAPI app with the custom functionality
defined in `CustomFastAPI` and `CustomOpenAPI` classes.
"""

from typing import Annotated, AsyncContextManager

from fastapi import Depends
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from application.api_utils.custom_fast_api import CustomFastAPI
from application.database.connection import get_session
from application.lifespan.app_lifespan import lifespan

app = CustomFastAPI(
    lifespan=lifespan,
    docs_url="/docs",
)

MAIN_DEPENDENCY = Annotated[
    AsyncContextManager[AsyncSession],
    Depends(get_session),
]

api_key_header = APIKeyHeader(name="api-key")
