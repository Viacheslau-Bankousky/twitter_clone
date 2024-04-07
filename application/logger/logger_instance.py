"""
This module sets up and initializes the application logger, 'app_logger'.

It sets the configuration for the logger using the settings in the
`logger_configuration`
from the `application.logger.configuration` module and uses these to
create an instance of the logger.

Modules:
--------
logging: Standard library module used for logging.
application.logger.configuration: Module containing the logger's
configurations.

Objects:
--------
app_logger: The configured logger instance.
Can be imported from this module.
"""

from logging import getLogger
from logging.config import dictConfig

from application.logger.configuration import logger_configuration

dictConfig(logger_configuration)
app_logger = getLogger("appLogger")
