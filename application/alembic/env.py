"""
This module is responsible for managing database migrations using Alembic.

The module is able to run migrations in both online and offline mode.
In online mode, it connects to the actual database and runs migrations,
while in offline mode it writes the SQL commands for the migrations to
a file without actually executing them.

Modules:
--------
- typing: Supports type hints.

- asyncio: A library to write concurrent code using the async/await syntax.

- os: This module provides a portable way of using operating system dependent
    functionality like reading environment variables.

- alembic.context: This module provides a context for migration scripts to
    operate in, which is passed as an argument to the command script.

- dotenv: This module reads the key-value pair from .env file and adds them
    to environment variable.

- models.base_model: This module contains the common database model

- sqlalchemy: The Python SQL toolkit and Object-Relational Mapping (ORM)
    system that gives application developers the full power and flexibility
    of SQL.

Functions:
----------
    run_migrations_offline():
        Run migrations in 'offline' mode where connection to actual database
        isn't available.
    do_run_migrations():
        Executes migrations within a given connection context.
    run_async_migrations():
        Executes migrations asynchronously within a connection context.
    run_migrations_online():
        Run migrations in 'online' mode where connection to actual database
        is available.
"""

import asyncio
import os
from logging.config import fileConfig
from typing import Optional

from alembic import context
from dotenv import load_dotenv
from models.base_model import Base  # type: ignore
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

load_dotenv()

DB_USER: str = os.environ["DB_USER"]
DB_PASSWORD: str = os.environ["DB_PASSWORD"]

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given
    string to the script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Execute migrations within a provided connection context.

    This function configures connection context and target metadata,
    begins a transaction and runs migrations on the provided connection.

    Args:
        connection (Connection):
            The connection to the database where migrations will be run.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Execute migrations asynchronously within a connection context.

    This function configures the connection URL with the database
    user and password, creates a connection using async SQLAlchemy
    engine, and runs the migrations asynchronously.
    After the migrations have been run, the connection to the
    database is closed.
    """
    url: Optional[str] = config.get_main_option("sqlalchemy.url")
    if url is not None:
        config.set_main_option(
            "sqlalchemy.url", url.format(DB_USER, DB_PASSWORD),
        )
        connectable = async_engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

        await connectable.dispose()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    This function runs the migrations asynchronously on an actual
    connection to the database.
    """
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
