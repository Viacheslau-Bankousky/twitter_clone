"""
This module provides a class, 'Handlers', which manages event handlers.

The key offering of this module is the 'Handlers' class.
It maintains a list of various application event handlers and offers
asynchronous methods for starting up and shutting down these handlers.

Modules:
--------
`dataclasses`: Specifically, `@dataclass` and `field`.
`@dataclass` is a decorator for creating data classes, and `field()`
declutters data class definitions.
`typing`: Specifically, `List` for typing the list objects.
`application.lifespan.handlers.abstract_handlers`: Specifically,
`ApplicationEventHandler` (An abstract base class for application event
handlers).
`application.lifespan.handlers.model_handlers`: Specifically, `ModelLoader`.
A handler class for loading models.

Classes:
--------
class Handlers
    A class to represent a collection of application event handlers.
"""

from dataclasses import dataclass, field
from typing import List

from application.lifespan.handlers.abstract_handlers import (
    ApplicationEventHandler,
)
from application.lifespan.handlers.model_handlers import ModelLoader


@dataclass
class EventHandler:
    """
    A class to represent a collection of application event handlers.

    Attributes
    ----------
    handlers : List[ApplicationEventHandler]
        a list of different application event handlers

    Methods
    -------
    add_handler(event_handler: ApplicationEventHandler):
        Adds a new handler to the handler's list.
    startup_all():
        An asynchronous method to start up all the handlers in the list.
    shutdown_all():
        An asynchronous method to shut down all the handlers in the list.
    """

    handlers: List[ApplicationEventHandler] = field(default_factory=list)

    def add_handler(self, event_handler: ApplicationEventHandler) -> None:
        """Add a new handler to the handler's list.

        Args:
            event_handler (ApplicationEventHandler): A handler to add.
        """
        self.handlers.append(event_handler)

    async def startup_all(self) -> None:
        """Start up all handlers in the handlers list asynchronously."""
        for event_handler in self.handlers:
            await event_handler.startup()

    async def shutdown_all(self) -> None:
        """Shut down all handlers in the handlers list asynchronously."""
        for event_handler in self.handlers:
            await event_handler.shutdown()


current_event_handler = EventHandler()
current_event_handler.add_handler(ModelLoader())
