"""
Module provides functions for hashing API keys and cleaning incoming data.

The module uses the hashlib for hashing API keys and bleach library for
cleaning incoming data.
The module also logs the actions using an application-level logger.

Modules:
--------
hashlib: Secure hashes and message digests
bleach: An easy whitelist-based HTML-sanitizing tool
application.logger.logger_instance: Instance of application logger
application.schemas.user_schemas: Schemas related to user data

Functions:
----------
hash_api_key(api_key: str) -> str:
    Takes an API key and returns the hashed version of the key.

shield_incoming_data(data: str) -> str:
    Clean the incoming data to remove any potentially harmful inputs.
"""

import hashlib

import bleach

from application.logger.logger_instance import app_logger


def hash_api_key(api_key: str) -> str:
    """
    Hash the provided API key using the SHA-256 algorithm.

    Args:
        api_key (str): The API key to be hashed.

    Returns:
        str: The hashed version of the provided API key.
    """
    app_logger.info("Hashing API key")
    return hashlib.sha256(api_key.encode()).hexdigest()


def shield_incoming_data(incoming_data: str) -> str:
    """
    Clean the provided data using the bleach library.

    Args:
        incoming_data (str): The data to be cleaned.

    Returns:
        str: The cleaned version of the provided data.
    """
    app_logger.info("Shielding incoming data")
    return bleach.clean(incoming_data)
