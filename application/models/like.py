"""
This module represents the `Like` entity.

It validates and manages operations like.

Classes:
--------
Like:
    Depicts `Like` entity with its fields and manipulative methods.

Modules:
--------
typing: Provides type hints compatibility.
sqlalchemy: SQL toolkit and ORM for Python that offers SQL's efficiency
and flexibility.
application.logger.logger_instance: Controls logging in the application.
application.models.associations: Contains various database association tables.
application.models.base_model: Carries the basic SQLAlchemy models' base.
application.models.tweet: Contains methods and fields for the 'Tweet' entity.
application.models.user: Houses methods and fields for the 'User' entity.

"""

from typing import Optional

from sqlalchemy import Column, Integer, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from application.errors.tweet_id_validation import TweetIdValidationError
from application.logger.logger_instance import app_logger
from application.models.associations import (
    tweets_likes_association,
    user_likes_association,
)
from application.models.base_model import Base
from application.models.tweet import Tweet
from application.models.user import User


class Like(Base):
    """
    Represents a 'Like' entity with fields and methods.

    Fields
    -------
    __tablename__ (str):
        The table name for the class.
    id (Integer):
        The identifier for a like.
    user_association (relationship):
        Many-to-many relationship with 'User' entity.
    tweet_association (relationship):
        Many-to-many relationship with 'Tweet' entity.

    """

    __tablename__ = "likes"
    id = Column(Integer, primary_key=True)
    user_association = relationship(
        "User",
        secondary=user_likes_association,
        back_populates="user_like_association",
    )
    tweet_association = relationship(
        "Tweet",
        secondary=tweets_likes_association,
        back_populates="like_association",
    )

    @classmethod
    async def add_like(
        cls,
        session: AsyncSession,
        tweet_id: int,
        user: User,
    ) -> None:
        """
        Add a new 'Like' entry for a tweet.

        This method can be used if the tweet has not been already
        liked by the user else previous like will be deleted

        Args:
            session (AsyncSession):
                The sqlalchemy session.
            tweet_id (int):
                The ID of the tweet to like.
            user (User):
                The User instance liking the tweet.

        Raises:
            TweetIdValidationError: If the tweet with the provided
                ID does not exist, a validation error is raised.
        """
        previously_liked: bool = await cls.has_like(
            session=session,
            tweet_id=tweet_id,
            user=user,
        )
        if previously_liked:
            await cls.delete_like(
                session=session,
                tweet_id=tweet_id,
                user=user,
            )
            return
        tweet: Optional[Tweet] = await cls.get_tweet_of_like(
            session=session,
            tweet_id=tweet_id,
        )
        if not tweet:
            raise TweetIdValidationError("Tweet does not exist.")
        app_logger.info("Like adding to the tweet")
        new_like: "Like" = cls()
        new_like.tweet_association.append(tweet)
        new_like.user_association.append(user)
        session.add(new_like)

    @classmethod
    async def get_tweet_of_like(
        cls,
        session: AsyncSession,
        tweet_id: int,
    ) -> Optional[Tweet]:
        """
        Return the 'Tweet' instance associated with the provided tweet id.

        This tweet is also associated with the 'Like' entity

        Args:
            session (AsyncSession):
                The sqlalchemy session.
            tweet_id (int):
                The ID of the tweet.

        Returns:
            Optional[Tweet]: An instance of 'Tweet' if found, else None.
        """
        app_logger.info("Getting the tweet of the specified like")
        tweet_result = await session.execute(
            select(Tweet).where(Tweet.id == tweet_id),
        )
        return tweet_result.scalars().first()

    @classmethod
    async def delete_like(
        cls,
        session: AsyncSession,
        tweet_id: int,
        user: User,
    ) -> None:
        """
        Delete the 'Like' instance for a tweet by a specific user.

        Args:
            session (AsyncSession):
                The sqlalchemy session.
            tweet_id (int):
                The ID of the tweet.
            user (User):
                The User instance who liked the tweet.
        """
        app_logger.info("Deleting the like")
        like: Optional["Like"] = await cls.take_like(
            session=session,
            tweet_id=tweet_id,
            user=user,
        )
        await session.delete(like)

    @classmethod
    async def take_like(
        cls,
        session: AsyncSession,
        tweet_id: int,
        user: User,
    ) -> Optional["Like"]:
        """
        Return the 'Like' instance for a tweet by a specific user.

        Args:
            session (AsyncSession):
                The sqlalchemy session.
            tweet_id (int):
                The ID of the tweet.
            user (User):
                The User instance who liked the tweet.

        Returns:
            Optional[Like]: The 'Like' instance if found, else None.
        """
        app_logger.info("Getting the like")
        like_result = await session.execute(
            select(cls)
            .where(cls.tweet_association.any(id=tweet_id))
            .where(cls.user_association.any(id=user.id)),
        )
        return like_result.scalars().first()

    @classmethod
    async def has_like(
        cls,
        session: AsyncSession,
        tweet_id: int,
        user: User,
    ) -> bool:
        """
        Check whether a user has liked a particular tweet.

        Args:
            session (AsyncSession):
                The sqlalchemy session.
            tweet_id (int):
                The ID of the tweet.
            user (User):
                The User instance.

        Returns:
            bool: True if the user has liked the tweet, else False.
        """
        like: Optional["Like"] = await cls.take_like(
            session=session,
            tweet_id=tweet_id,
            user=user,
        )
        return bool(like)
