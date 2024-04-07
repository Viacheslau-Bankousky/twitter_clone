"""
This module outlines an abstract Base class for SQLAlchemy models.

Classes:
--------
Base:
    Abstract base class for all SQLAlchemy declarative models
    in the application.

Modules:
--------
sqlalchemy.ext.asyncio: Provides asyncio support to SQLAlchemy.
sqlalchemy.orm: Provides ORM (Object Relational Mapper) support.
"""

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase  # type: ignore


class Base(DeclarativeBase, AsyncAttrs):
    """
    An abstract base class.

    Inherits:
        DeclarativeBase: Basic class which other classes can inherit from
        and gain a mapping from classes to Relational Database tables.
        AsyncAttrs: Adds asyncio compatibility to the DeclarativeBase.

    Attributes:
        __abstract__(bool): This attribute tells SQLAlchemy that this class
        is an abstract base class and not to be mapped to a database table.
    """

    __abstract__ = True
