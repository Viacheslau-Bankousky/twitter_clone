"""
A Python module that configures logger for the application.

This module provides a dictionary config (`logger_configuration`),
which sets up the format, handlers, and loggers settings for logging
in this application.

The logging configuration is set up to have at most three handlers:
1. `consoleHandler` which sends logs to stdout.
2. `infoFileHandler` which outputs INFO and higher level logs to a log
file (normal_activity.log).
3. `errorFileHandler` which outputs ERROR and higher level logs to
another log file (errors.log).

Modules:
--------
sys - provides functions and variables used to manipulate different
parts of the Python runtime environment.

Details:
--------
Loggers:
  appLogger: prints information from the application.

Handlers:
  consoleHandler: logs DEBUG and higher severity errors into the console.
  infoFileHandler: logs INFO and higher severity errors into the
  normal_activity.log file.
  errorFileHandler: logs ERROR and higher severity errors into the
  error.log file.

Formatters:
  fileFormatter: specifies the layout for each logger message
  (including the timestamp, the module, and function where the logging
  call was made, the severity and the actual message) for file output logs.
  consoleFormatter: specifies the layout for logger messages (including the
  severity level and actual message) for console output logs.
"""

import sys

LEVEL: str = "level"
FILE_FORMAT: str = "%(asctime)s - %(module)s.%(funcName)s - %(levelname)s - %(message)s"  # noqa: WPS323,E501
CONSOLE_FORMAT: str = "%(levelname)s - %(message)s"  # noqa: WPS323
DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%S%Z"  # noqa: WPS323

logger_configuration = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "fileFormatter": {
            "format": FILE_FORMAT,
            "datefmt": DATE_FORMAT,
        },
        "consoleFormatter": {
            "format": CONSOLE_FORMAT,
            "datefmt": DATE_FORMAT,
        },
    },
    "handlers": {
        "consoleHandler": {
            "class": "logging.StreamHandler",
            LEVEL: "INFO",
            "formatter": "consoleFormatter",
            "stream": sys.stdout,
        },
        "infoFileHandler": {
            "class": "logging.FileHandler",
            LEVEL: "INFO",
            "formatter": "fileFormatter",
            "filename": "application/logs/normal_activity.log",
        },
        "errorFileHandler": {
            "class": "logging.FileHandler",
            LEVEL: "ERROR",
            "formatter": "fileFormatter",
            "filename": "application/logs/errors.log",
        },
    },
    "loggers": {
        "appLogger": {
            LEVEL: "DEBUG",
            "handlers": [
                "consoleHandler",
                "infoFileHandler",
                "errorFileHandler",
            ],
            "qualname": "appLogger",
            "propagate": False,
        },
    },
}
