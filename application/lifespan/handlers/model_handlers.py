"""
This module manages the loading of application models.

The `ModelLoader` class, a subclass of `ApplicationEventHandler`,
is responsible for the loading of application models.
During the startup of the application, it connects to the database
engine and loads the model's metadata.
At the shutdown of the application, it logs the shutdown process
and disposes the connection to the engine.

Modules:
--------
application.database.connection: Connects to the database.
application.lifespan.handlers.abstract_handlers.ApplicationEventHandler:
Framework for building application event handlers.
application.logger.logger_instance: Handles the logging within
the application.
application.models.base_model: Provides the base model.
application.models.like: Provides the `Like` model.
application.models.media: Provides the `Media` model.
application.models.tweet: Provides the `Tweet` model.

Classes:
--------
ModelLoader:
    A handler for loading of application models.
"""

from application.database.connection import engine
from application.lifespan.handlers.abstract_handlers import (
    ApplicationEventHandler,
)
from application.logger.logger_instance import app_logger
from application.models.base_model import Base
from application.models.like import Like  # noqa: F401
from application.models.media import Media  # noqa: F401
from application.models.tweet import Tweet  # noqa: F401


class ModelLoader(ApplicationEventHandler):
    """Handles the loading of application models.

    Inherits methods from the ApplicationEventHandler
    abstract base class.

    Attributes:
    -----------
    None

    Methods:
    ----------
    startup() -> None: Calls at the startup event.
                        Connects to the engine and
                        loads the metadata of models.

    shutdown() -> None: Calls at the shutdown event.
                        Logs the shutdown process
                        and disposes the engine.
    """

    async def startup(self) -> None:
        """Carries out initialization tasks.

        Connects to engine and loads the metadata,
        logging the start of the process.
        """
        async with engine.begin() as connection:
            app_logger.info("Model Loader Started")
            await connection.run_sync(Base.metadata.create_all)

    async def shutdown(self) -> None:
        """Carries out shutdown tasks.

        Logs shutdown process, and disposes the engine.
        """
        app_logger.info("Model Loader Stopped")
        await engine.dispose()
