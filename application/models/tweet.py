"""
This module represents the `Tweet` class and its operations.

Classes:
--------
Tweet:
    Represents a tweet in a social media platform, with functionalities
    such as adding a tweet, retrieving a tweet and deleting a tweet.

Modules:
--------
typing: Provides runtime support for type hints.
sqlalchemy: The Python SQL toolkit and Object-Relational Mapping.
sqlalchemy.orm: Provides features for interacting and working with
SQLAlchemy ORM.
sqlalchemy.orm.exc: Exception classes for SQLAlchemy ORM.
application.errors.media_id_validation: Validates associated media ID
in a tweet.
application.errors.tweet_id_validation: Validates tweet ID.
application.logger.logger_instance: Handles logging in the application.
application.models.associations: Contains various DB association tables.
application.models.base_model: Contains base SQLAlchemy models.
application.models.media: Represents a media associated with a tweet.
application.models.user: Represents a user associated with a tweet.

"""

import os
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload
from sqlalchemy.orm.exc import NoResultFound

from application.errors.media_id_validation import MediaIdValidationError
from application.errors.tweet_id_validation import TweetIdValidationError
from application.logger.logger_instance import app_logger
from application.models.associations import (
    tweets_likes_association,
    tweets_media_association,
    user_tweets_association,
)
from application.models.base_model import Base
from application.models.media import Media
from application.models.user import User

if TYPE_CHECKING:
    from application.models.like import Like  # noqa: F401


class Tweet(Base):
    """The 'Tweet' class represents a Tweet on the social media platform.

    Fields:
    -------
    __tablename__ (str):
        The table name for the class.
    id (Int):
        The id of the Tweet.
    tweet_data (Str):
        The data/content of the Tweet.
    user_association (relationship):
        Association with User class.
    like_association (relationship):
        Association with Like class.
    media_association (relationship):
        Association with Media class.
    """

    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True)
    tweet_data = Column(String)
    user_association = relationship(
        "User",
        secondary=user_tweets_association,
        back_populates="user_tweet_association",
    )
    like_association = relationship(
        "Like",
        secondary=tweets_likes_association,
        back_populates="tweet_association",
    )
    media_association = relationship(
        "Media",
        secondary=tweets_media_association,
        back_populates="tweet_association",
    )

    @classmethod
    async def add_tweet(
        cls,
        session: AsyncSession,
        tweet_data: str,
        tweet_media_ids: Optional[List[int]],
        user: User,
    ) -> Optional[int]:
        """
        Add a new tweet, along with optional associated media, to the database.

        This method will create a new tweet instance and adds it
        to the session.
        If `tweet_media_ids` are given, the method attempts to retrieve all the
        related media instances.
        If no related media are found, a `MediaIdValidationError` is raised
        and the tweet is not added.

        Args:
            session (AsyncSession):
                The session for asynchronous database operations.
            tweet_data (str):
                The content of the new tweet.
            tweet_media_ids (Optional[List[int]]):
                List of IDs of associated media.
                If provided, the method tries to retrieve all the related media
                instances.
                If any of them are not found, a
                `MediaIdValidationError` exception is raised.
            user (User):
                The user that creates the new tweet.
                The new tweet is associated to this user.

        Raises:
            MediaIdValidationError: If `tweet_media_ids` is provided and no
                media with the given IDs are found.

        Returns:
            int: The ID of the newly added tweet or None if id
            of media invalid.
        """
        app_logger.info("Adding Tweet")
        new_tweet = cls(tweet_data=tweet_data, user_association=[user])
        if tweet_media_ids:
            media_objects: Optional[List[Media]] = await Media.get_all_media(
                session=session,
                tweet_media_ids=tweet_media_ids,
            )
            app_logger.info(media_objects)
            if media_objects is None:
                app_logger.exception("No media objects found")
                raise MediaIdValidationError("No media objects found")
            new_tweet.media_association.extend(media_objects)
        session.add(new_tweet)
        await session.flush()
        return new_tweet.id

    @classmethod
    async def take_tweet(
        cls,
        session: AsyncSession,
        tweet_id: int,
        user: "User",
    ) -> Optional["Tweet"]:
        """
        Retrieve a specific tweet from the database.

        This function fetches a tweet based on its ID.
        After fetching the tweet, it checks if the tweet belongs
        to the given user based on user_association.
        If the tweet does not belong to the user, it returns None.

        Args:
            session (AsyncSession):
                The session for async database operations
            tweet_id (int):
                The ID of the tweet to retrieve
            user (User):
                The User instance for which the tweet ownership is to
                be checked

        Returns:
            Tweet: The retrieved tweet if it belongs to the given user,
            otherwise None.
        """
        from application.models.like import Like  # noqa: WPS474

        app_logger.info("Getting Tweet")
        tweet_result = await session.execute(
            select(cls)  # type: ignore
            .options(
                selectinload(cls.media_association),
                selectinload(cls.like_association).joinedload(
                    Like.user_association,
                ),
                selectinload(cls.user_association),
            )
            .filter(cls.id == tweet_id),
        )
        try:
            tweet: Optional[Tweet] = tweet_result.scalar_one()
        except NoResultFound:
            app_logger.exception("Tweet not found")
            return None

        return tweet if tweet.user_association[0].id == user.id else None

    @classmethod
    async def delete_tweet(
        cls,
        session: AsyncSession,
        tweet_id: int,
        user: "User",
    ) -> None:
        """
        Delete a specific tweet from the database.

        This method will first attempt to retrieve the tweet with the given ID
        from the database that belongs to a given user.
        If the tweet is not found or does not belong to the user, None will be
        returned from the 'take_tweet' method.
        If None is returned, a `TweetIdValidationError` is raised.
        If the tweet has associated media, the media files are deleted from the
        disk, and the media records are deleted from the database.
        Also, if users liked the tweet, each like would be deleted from the
        database.

        Args:
            session (AsyncSession):
                The session for asynchronous database operations.
            tweet_id (int):
                The ID of the tweet to be deleted.
            user (User):
                The user instance to check the ownership of the tweet.

        Raises:
            TweetIdValidationError: If no tweet with the provided ID is found,
                or it does not belong to the user.

        Return:
            None
        """
        app_logger.info("Deleting Tweet")
        tweet: Optional["Tweet"] = await cls.take_tweet(
            session=session,
            tweet_id=tweet_id,
            user=user,
        )
        if tweet is None:
            raise TweetIdValidationError("Tweet not found")
        media_association: Optional[List[Media]] = tweet.media_association

        if media_association is not None:
            await cls.delete_associated_media(
                media_association=media_association,
                session=session,
            )
        like_association: Optional[List["Like"]] = tweet.like_association
        if like_association is not None:
            await cls.delete_associated_likes(
                like_association=like_association,
                session=session,
                tweet_id=tweet.id,
            )

        await session.delete(tweet)
        await session.flush()

    @classmethod
    async def delete_associated_media(
        cls,
        session: AsyncSession,
        media_association: List[Media],
    ) -> None:
        """
        Delete associated media entities.

        This method first validates if a media file exists on disk for each
        media entity in the given list.
        If a media file exists, it is deleted from the disk and its
        corresponding ID is added to a list of media IDs.
        Finally, all media records associated with these IDs are deleted
        from the database.

        Args:
            session (AsyncSession):
                The active sqlalchemy session for asynchronous database
                operations.
            media_association (List[Media]):
                A list of media entities that are to be deleted.

        Return:
            None
        """
        media_ids = []
        for media in media_association:
            if media.file is not None:
                Media.delete_media_from_disk(
                    path_to_file=os.path.join("saved_photos", media.file),
                )
                media_ids.append(media.id)

        await Media.delete_media_from_db_by_ids(
            session=session,
            media_ids=media_ids,
        )

    @classmethod
    async def delete_associated_likes(
        cls,
        like_association,
        session: AsyncSession,
        tweet_id: int,
    ) -> None:
        """
        Delete associated 'likes' entities.

        This method goes through each 'like' association in the provided list
        and deletes each 'like' from the database using the ID of the tweet
        and the associated user information.

        Args:
            like_association:
                A list of 'like' associations that are to be deleted.
            session (AsyncSession):
                The active sqlalchemy session for asynchronous database
                operations.
            tweet_id (int):
                The ID of the tweet whose 'likes' are to be deleted.

        Return:
            None
        """
        from application.models.like import Like  # noqa: WPS474

        for like in like_association:
            await Like.delete_like(
                session=session,
                tweet_id=tweet_id,
                user=like.user_association[0],
            )
