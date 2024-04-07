"""
A module represents the `Media` class.

Classes:
--------
Media:
    Embodies media files, imparting them the ability to perform actions s
    uch as validation, storage, deletion, and retrieval from the database.

Modules:
--------
asyncio: Offers asynchronous I/O primitives for managing various types
of I/O operations.
io: Provides core tools for working with streams.
os: Offers a portable way of using operating system-dependent functionality.
typing: Supports type hints.
uuid: Implies the UUID objects as per RFC 4122 and DCE 1.1: Authentication
and Security Services.
fastapi: Starlette-based web app framework, allowing for async request
handling.
PIL: Adds support for opening, manipulating, and saving images.
sqlalchemy: SQL toolkit and ORM that offers SQL's bounties and flexibility.
"""

import asyncio
import io
import os
from typing import TYPE_CHECKING, List, Optional
from uuid import uuid4

from fastapi import UploadFile
from PIL import Image, UnidentifiedImageError
from sqlalchemy import Column, Integer, String, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from application.errors.image_validation import ImageValidationError
from application.logger.logger_instance import app_logger
from application.models.associations import tweets_media_association
from application.models.base_model import Base

if TYPE_CHECKING:
    from application.models.tweet import Tweet  # noqa: F401


class Media(Base):
    """
    A class that represents media files in the application.

    This class provides several class methods that allow you
    to interact with the media files in the application,
    including getting all media, validating images, saving
    media to disk, deleting media from disk and database,
    and adding media to the database.

    Fields
    -------
    __tablename__ (str):
        The table name for the class.
    id (int):
        Unique id of the media file.
    file (str):
        Associated file of the media.
    tweet_association (relationship):
        Many-to-many relationship with 'Tweet' entity.

    """

    __tablename__ = "media"
    id = Column(Integer, primary_key=True)
    file = Column(String)  # noqa: WPS110
    tweet_association = relationship(
        "Tweet",
        secondary=tweets_media_association,
        back_populates="media_association",
    )

    @classmethod
    async def get_all_media(
        cls,
        session: AsyncSession,
        tweet_media_ids: List[int],
    ) -> Optional[List["Media"]]:
        """
        Retrieve all media associated with a tweet.

        Args:
            session (AsyncSession):
                The database session for making queries.
            tweet_media_ids (List[int]):
                A list of ids of the media to retrieve.

        Returns:
            A list of Media instances associated with the IDs.
            If there are missing media, an error is logged and
            `None` is returned.
        """
        app_logger.info("Getting all media from the Tweet")
        media_result: Optional[List["Media"]] = (
            (
                await session.execute(
                    select(cls).where(cls.id.in_(tweet_media_ids)),
                )
            )
            .scalars()
            .all()
        )
        if media_result is None or len(media_result) != len(tweet_media_ids):
            app_logger.exception("Error getting all media from the Tweet")
            return None
        return media_result

    @classmethod
    def is_image(cls, binary_data: bytes) -> bool:
        """
        Validate whether provided binary data represents a valid image.

        Args:
            binary_data (bytes):
                The binary data to be validated as an image.

        Returns:
            True if the binary data represents a valid image, otherwise False.
        """
        app_logger.info("Checking if image is valid")
        try:
            with Image.open(io.BytesIO(binary_data)) as image:
                image.verify()
                app_logger.info("Image is valid")
                return True
        except (IOError, SyntaxError, UnidentifiedImageError):
            app_logger.exception("Image is not valid")
            return False

    @classmethod
    def save_media(cls, filename: str, media_data: bytes) -> str:
        """
        Save media data to a file in disk.

        Args:
            filename (str):
                The original filename of the media.
            media_data (bytes):
                The media data in bytes to be saved.

        Returns:
            str: unique name of the media file.
        """
        app_logger.info("Saving image")
        unique_filename: str = "{0}.{1}".format(
            str(uuid4()),
            filename.split(".")[-1],
        )
        filename_path: str = os.path.join("saved_photos", unique_filename)

        with open(filename_path, "wb") as file_object:
            file_object.write(media_data)
        return unique_filename

    @classmethod
    def delete_media_from_disk(cls, path_to_file: str) -> None:
        """
        Delete media file from disk.

        Args:
            path_to_file (str):
                The filepath of the media to be deleted.

        Exceptions:
            OSError: An error occurred accessing the media file.
        """
        app_logger.info("Deleting image")
        try:
            os.remove(path_to_file)
        except OSError as exc:
            app_logger.exception(
                "Error: {0} : {1}".format(path_to_file, exc.strerror),
            )

    @classmethod
    async def delete_media_from_db_by_ids(
        cls,
        session: AsyncSession,
        media_ids: List[int],
    ) -> None:
        """
        Delete media entries from the database by ids.

        Args:
            session (AsyncSession):
                The database session for making queries.
            media_ids (List[int]):
                A list of ids of the media entries to
                delete.
        """
        app_logger.info("Deleting media from database by IDs")
        await session.execute(
            delete(cls.__table__).where(cls.id.in_(media_ids)),
        )
        await session.flush()

    @classmethod
    async def add_media_to_database(
        cls,
        session: AsyncSession,
        media: UploadFile,
    ) -> Optional[int]:
        """
        Attempt to add a new media to the database.

        Before adding, this method validates if the media is a valid image
        file.

        Args:
            session (AsyncSession):
                The database session for making queries.
            media (UploadFile):
                The media file to add to the database.

        Returns:
            int: The id of the created media entry in the database
            or `None` if the media is not valid.

        Raises:
            ImageValidationError: The media is not a valid image file.
        """
        app_logger.info("Adding media to database")
        media_data = await media.read()
        if await asyncio.to_thread(cls.is_image, media_data):
            media_file_name: str = await asyncio.to_thread(
                cls.save_media,
                media.filename if media.filename else "media.jpg",
                media_data,
            )
            new_media: "Media" = cls(file=media_file_name)
            session.add(new_media)
            await session.flush()
            return new_media.id

        app_logger.exception("Media is not valid")
        raise ImageValidationError("File is not an image")
