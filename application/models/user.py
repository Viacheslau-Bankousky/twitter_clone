"""
This module represents the `User` class and its operations.

Classes:
--------
User:
    Represents a user with functionalities like adding a user,
    getting a user
    information, following/unfollowing a user, and retrieving
    a user's data.

Modules:
--------
typing: Provides runtime support for type hints
sqlalchemy: The Python SQL toolkit and Object-Relational Mapping
for Python
application.errors.self_following_validation: Check validation for
self following
application.errors.self_unfollowing_validation: Validates for
self unfollowing
application.errors.user_id_validation: Validates user ID
application.logger.logger_instance: Handles logging in the application
application.models.associations: Contains various DB association tables
application.models.base_model: Contains base SQLAlchemy models
application.schemas.user_schemas: Contains schemas for the 'User' entity
"""

from typing import TYPE_CHECKING, List, NewType, Optional, Tuple, Union

from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import backref, joinedload, relationship, subqueryload

from application.errors.self_following_validation import (
    SelfFollowingValidationError,
)
from application.errors.self_unfollowing_validation import (
    SelfUnFollowingValidationError,
)
from application.errors.user_id_validation import UserIdValidationError
from application.logger.logger_instance import app_logger
from application.models.associations import (
    subscription_table,
    user_likes_association,
    user_tweets_association,
)
from application.models.base_model import Base
from application.schemas.tweet_schemas import Tweet as TweetSchema
from application.schemas.user_schemas import User as UserSchema
from application.schemas.user_schemas import (
    UserConnections as UserConnectionsSchema,
)
from application.schemas.user_schemas import UserResponse

if TYPE_CHECKING:
    from application.models.like import Like, Tweet  # noqa: F401

USER_NOT_FOUND_ERROR_MSG: str = "User not found"

tweet_description = NewType("tweet_description", Tuple[int, str, "Tweet"])


class User(Base):
    """
    Represents a User in the social media platform.

    This class provides several class methods that in line with the User's
    representative role, including adding a user into the application, getting
    a user by API key or ID, creating a follow/unfollow relationship and
    getting the profile of a user.

    Fields:
    -------
    __tablename__ (str):
        The table name for the class.
    id (int):
        Unique id of the user.
    name (str):
        The name of the user.
    api_key (str):
        API key associated with the user.
    user_tweet_association (relationship):
        Many-to-many relationship with 'Tweet' entity.
    user_like_association(relationship):
        Many-to-many relationship with 'Like' entity.
    followed(relationship):
        Many-to-many relationship with 'User' entity,
        indicating the users this user is following.

    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    api_key = Column(String, nullable=False, unique=True, index=True)
    user_tweet_association = relationship(
        "Tweet",
        secondary=user_tweets_association,
        back_populates="user_association",
    )
    user_like_association = relationship(
        "Like",
        secondary=user_likes_association,
        back_populates="user_association",
    )
    followed = relationship(
        "User",
        secondary=subscription_table,
        primaryjoin=(subscription_table.c.follower_id == id),
        secondaryjoin=(subscription_table.c.followed_id == id),
        backref=backref("followers"),
    )

    @classmethod
    async def add_user(
        cls,
        session: AsyncSession,
        api_key: str,
        name: str,
    ) -> Optional[int]:
        """
        Create a new user with the given API key and name.

        Args:
            session (AsyncSession):
                SQLAlchemy session.
            api_key (str):
                The unique key associated with the user.
            name (str):
                The name of the user.

        Returns:
            id (int): The ID of the newly created user
            or None if the user with passed data already exists
            (an appropriate exception will be risen and processed by
            exception middleware).
        """
        app_logger.info("Adding user")
        new_user = cls(name=name, api_key=api_key)
        session.add(new_user)
        await session.flush()
        return new_user.id

    @classmethod
    async def get_user_by_api_key(
        cls,
        session: AsyncSession,
        api_key: str,
    ) -> Optional["User"]:
        """
        Retrieve a User instance from database by its API key.

        Args:
            session (AsyncSession):
                SQLAlchemy session to connect to the database.
            api_key (str):
                The API key attached to the user.

        Returns:
            Optional[User]: Returns User instance if found, else None.
        """
        app_logger.info("Getting user by api_key")
        stmt = select(cls).where(cls.api_key == api_key)
        user_result = await session.execute(stmt)
        return user_result.scalars().first()

    @classmethod
    async def get_user_by_id(
        cls,
        session: AsyncSession,
        user_id: int,
    ) -> Optional["User"]:
        """
        Retrieve a User instance by its ID.

        Args:
            session (AsyncSession):
                SQLAlchemy session to connect to the database.
            user_id (int):
                The ID of the user.

        Raises:
            UserIdValidationError: Error when user is not found
                by the specified ID.

        Returns:
            Optional[User]: Returns User instance if found, else None.
        """
        app_logger.info("Getting user by id")
        user_result = await session.execute(
            select(cls).where(cls.id == user_id),
        )
        user: Optional["User"] = user_result.scalars().first()
        if user is None:
            app_logger.exception("User not found")
            raise UserIdValidationError(USER_NOT_FOUND_ERROR_MSG)
        app_logger.info("User found")
        return user

    @classmethod
    async def get_user_with_eager_load(
        cls,
        session: AsyncSession,
        user_id: int,
    ) -> "User":
        """
        Retrieve a User instance along with its related data.

        It means an eager Loading of followed

        Args:
            session (AsyncSession):
                SQLAlchemy session to connect to the database.
            user_id (int):
                The ID of the user.

        Returns:
            User: User instance with its related data
        """
        app_logger.info("Eager loading of user's related data")
        user_result = await session.execute(
            select(cls)
            .options(joinedload(cls.followed))  # type: ignore
            .filter_by(id=user_id),
        )
        return user_result.unique().first()[0]

    @classmethod
    async def follow_user(
        cls,
        session: AsyncSession,
        user_to_follow_id: int,
        current_user: "User",
    ) -> None:
        """
        Let the current user follow another user.

        Args:
            session (AsyncSession):
                SQLAlchemy session to connect to the database.
            user_to_follow_id (int):
                The ID of the user that current user wants to follow.
            current_user (User):
                The instance of the current user.

        Raises:
            SelfFollowingValidationError: an attempt to follow themselves.
            UserIdValidationError: Error when user to follow is not found.
        """
        app_logger.info("Following user")
        if current_user.id == user_to_follow_id:
            raise SelfFollowingValidationError("Cannot follow yourself")
        user_to_follow: Optional["User"] = await cls.get_user_by_id(
            session=session,
            user_id=user_to_follow_id,
        )
        if user_to_follow is None:
            raise UserIdValidationError(USER_NOT_FOUND_ERROR_MSG)
        current_user_with_eager_loaded_attr: "User" = (
            await cls.get_user_with_eager_load(
                session=session,
                user_id=current_user.id,
            )
        )
        current_user_with_eager_loaded_attr.followed.append(user_to_follow)
        session.add(current_user_with_eager_loaded_attr)

    @classmethod
    async def unfollow_user(
        cls,
        session: AsyncSession,
        user_to_unfollow_id: int,
        current_user: "User",
    ) -> None:
        """
        Let the current user unfollow another user.

        Args:
            session (AsyncSession):
                SQLAlchemy session to connect to the database.
            user_to_unfollow_id (int):
                The ID of the user that current user wants to unfollow.
            current_user (User):
                The instance of the current user.

        Raises:
            SelfUnFollowingValidationError: an attempt to unfollow themselves.
            UserIdValidationError: Error when user to unfollow is not found.
        """
        app_logger.info("Unfollowing user")
        if user_to_unfollow_id == current_user.id:
            raise SelfUnFollowingValidationError("Cannot unfollow yourself")
        user_to_unfollow: Optional["User"] = await cls.get_user_by_id(
            session=session,
            user_id=user_to_unfollow_id,
        )
        if user_to_unfollow is None:
            raise UserIdValidationError(USER_NOT_FOUND_ERROR_MSG)
        current_user_with_eager_loaded_attr: "User" = (
            await cls.get_user_with_eager_load(
                session=session,
                user_id=current_user.id,
            )
        )
        current_user_with_eager_loaded_attr.followed.remove(
            user_to_unfollow,
        )
        session.add(current_user_with_eager_loaded_attr)

    @classmethod
    async def get_actual_data_of_current_user(
        cls,
        session: AsyncSession,
        user: "User",
    ) -> Optional[UserResponse]:
        """
        Retrieve the actual data of the current logged in user.

        Args:
            session (AsyncSession):
                SQLAlchemy session to connect to the database.
            user (User):
                The instance of the current user.

        Returns:
            Optional[UserResponse]: Returns User schema if found,
            else None (if an exception occurred).
        """
        app_logger.info("Getting actual data of current user")
        user_with_actual_data: "User" = (
            await cls.get_actual_data_of_user(  # type: ignore
                session=session,
                user_id=user.id,
            )
        )
        return cls.get_user_schema(user=user_with_actual_data)

    @classmethod
    async def get_actual_data_of_user_by_id(
        cls,
        session: AsyncSession,
        user_id: int,
    ) -> Optional[UserResponse]:
        """
        Retrieve the actual data of a user by its ID.

        Args:
            session (AsyncSession):
                SQLAlchemy session to connect to the database.
            user_id (int):
                The ID of the user.

        Raises:
            UserIdValidationError: Error when user is not found.

        Returns:
            Optional[UserResponse]: Returns User instance if found,
            else None.
        """
        app_logger.info("Getting actual data of user by id")
        user: Optional["User"] = await cls.get_actual_data_of_user(
            session=session,
            user_id=user_id,
        )
        if user is None:
            raise UserIdValidationError(USER_NOT_FOUND_ERROR_MSG)
        return cls.get_user_schema(user=user)

    @classmethod
    async def get_actual_data_of_user(
        cls,
        session: AsyncSession,
        user_id: int,
    ) -> Optional["User"]:
        """
        Retrieve a user along with its related data.

        It means eager loading of followers and followed of the user

        Args:
            session (AsyncSession):
                SQLAlchemy session to connect to the database.
            user_id (int):
                The ID of the user.

        Returns:
            Optional[User]: Returns User instance if found, else None.
        """
        stmt = (
            select(cls)
            .options(joinedload(cls.followed))  # type: ignore
            .options(joinedload(cls.followers))
            .where(cls.id == user_id)
        )
        user_result = await session.execute(stmt)
        return user_result.scalars().first()

    @classmethod
    def get_user_schema(cls, user: "User") -> UserResponse:
        """
        Construct a UserResponse object from a User instance.

        Args:
            user (Optional[User]):
                The instance of the user.

        Returns:
            UserResponse: The constructed UserResponse object with
            User details.
        """
        app_logger.info("Getting user schema")
        return UserResponse(
            user=UserSchema(
                id=user.id,
                name=user.name,
                followers=[
                    UserConnectionsSchema(id=follower.id, name=follower.name)
                    for follower in user.followers
                ],
                following=[
                    UserConnectionsSchema(id=followed.id, name=followed.name)
                    for followed in user.followed
                ],
            ),
        )

    @classmethod
    async def get_all_tweets(
        cls,
        session: AsyncSession,
        user: "User",
    ) -> List[TweetSchema]:
        """
        Retrieve all tweets of the users that the given user follows.

        Args:
            session (AsyncSession):
                The session for asynchronous database operations.
            user (User):
                The user of interest.

        Returns:
            List[TweetSchema]: A list of Tweet schemas representing the tweets
                of the users that the given user follows.
        """
        current_user_with_related_objects: "User" = (
            await cls.get_user_with_eager_load(
                session=session,
                user_id=user.id,
            )
        )
        tweets_of_current_user_followed: Optional[List[tweet_description]] = (
            await cls.take_tweets_of_current_user_followed(
                session=session,
                user_with_related_objects=current_user_with_related_objects,
            )
        )
        app_logger.info("Showing user's tweets")
        return cls.get_list_of_tweet_schemas(
            tweets=tweets_of_current_user_followed,
        )

    @classmethod
    async def take_tweets_of_current_user_followed(
        cls,
        user_with_related_objects: "User",
        session: AsyncSession,
    ) -> Optional[List[tweet_description]]:
        """
        Get sorted tweets of users that the current user follows.

        Args:
            user_with_related_objects (User):
                User object carrying related objects.
            session (AsyncSession):
                The session for asynchronous database operations.

        Returns:
            Optional[List[tweet_description]: List of tuples containing
            details of tweets of users followed by the current user, or None
            if there are no such tweets.
        """
        from application.models.like import Like  # noqa: F811, WPS474
        from application.models.tweet import Tweet

        user_followed_ids: List[int] = [
            user.id for user in user_with_related_objects.followed
        ]
        tweets_result = await session.execute(
            select(Tweet)
            .options(  # type: ignore
                subqueryload(Tweet.user_association),
                subqueryload(Tweet.media_association),
                subqueryload(Tweet.like_association).joinedload(
                    Like.user_association,
                ),
            )
            .filter(Tweet.user_association.any(cls.id.in_(user_followed_ids))),
        )
        tweets: Optional[List[Tweet]] = tweets_result.scalars().all()
        if tweets is not None:
            return cls.make_list_of_sorted_tweets(tweets_list=tweets)
        app_logger.info("Tweets of current user are not followed")
        return None

    @classmethod
    def make_list_of_sorted_tweets(
        cls,
        tweets_list: List["Tweet"],
    ) -> List[tweet_description]:
        """
        Make a list of sorted tweets.

        Args:
            tweets_list (List[Tweet]):
                List of tweet objects.

        Returns:
            List[tweet_description]: A list of tuples containing
            details of sorted tweets.
        """
        unsorted_tweets: List[tweet_description] = [
            (  # type: ignore
                tweet.user_association[0].id,
                tweet.user_association[0].name,
                tweet,
            )
            for tweet in tweets_list
        ]
        return cls.sort_tweets(tweets=unsorted_tweets)

    @classmethod
    def sort_tweets(
        cls,
        tweets: List[tweet_description],
    ) -> List[tweet_description]:
        """
        Sort tweets in descending order based on the number of likes.

        Args:
            tweets (tweet_description):
                List of tuples containing tweet details.

        Returns:
            List[tweet_description]: A list of sorted tweets in tuples.
        """
        return sorted(
            tweets,
            key=lambda tweet: len(tweet[2].like_association),
            reverse=True,
        )

    @classmethod
    def get_list_of_tweet_schemas(
        cls,
        tweets: Optional[List[tweet_description]],
    ) -> Union[List, List[TweetSchema]]:
        """
        Get a list of Tweet schemas.

        Args:
            tweets (Optional[List[tweet_description]]):
                List of tuples containing tweet details.

        Returns:
            Union[List, List[TweetSchema]]: A list of Tweet schemas.
        """
        if tweets is not None:
            return [
                TweetSchema(
                    id=tweet[2].id,
                    content=str(tweet[2].tweet_data),
                    attachments=[
                        "/images/{0}".format(media.file)
                        for media in tweet[2].media_association
                    ],
                    author=UserConnectionsSchema(id=tweet[0], name=tweet[1]),
                    likes=[
                        UserConnectionsSchema(
                            id=liked_user.id,
                            name=liked_user.name,
                        )
                        for like in tweet[2].like_association
                        for liked_user in like.user_association
                    ],
                )
                for tweet in tweets
            ]
        app_logger.info("Tweets of current user are not followed")
        return []
