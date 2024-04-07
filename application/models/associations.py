"""
This module creates various association tables.

Tables:
--------
user_likes_association: Defines a many-to-many relationship between
users and likes.
tweets_likes_association: Establishes a many-to-many relationship
between tweets and likes.
tweets_media_association: Defines a many-to-many relationship
between tweets and media.
user_tweets_association: Associates a many-to-many relationship
between users and tweets.
subscription_table: Represents a many-to-many relationship for user
subscriptions.

Modules:
--------
sqlalchemy: SQL toolkit and Object-Relational Mapping (ORM) system
for Python.
application.models.base_model: Provides the `Base` SQLAlchemy
declarative base class.

Attributes:
-----------
user_id (int): Identifier for a user.
Acts as a foreign key to 'users.id'.
like_id (int): Identifier for a like. Acts as a foreign key
to 'likes.id'.
tweet_id (int): Identifier for a tweet. Acts as a foreign key
to 'tweets.id'.
media_id (int): Identifier for media. Acts as a foreign key
to 'media.id'.
follower_id (int): Represents the identifier for a follower.
Acts as a foreign key to 'users.id'.
followed_id (int): Represents the identifier for the followed user.
Acts as a foreign_key to 'users.id'.
"""

from sqlalchemy import Column, ForeignKey, Integer, Table, UniqueConstraint

from application.models.base_model import Base

user_likes_association = Table(
    "user_likes",
    Base.metadata,
    Column(
        "user_id",
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
    Column(
        "like_id",
        Integer,
        ForeignKey(
            "likes.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
    UniqueConstraint("user_id", "like_id"),
)

tweets_likes_association = Table(
    "tweets_likes",
    Base.metadata,
    Column(
        "tweet_id",
        Integer,
        ForeignKey(
            "tweets.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
    Column(
        "like_id",
        Integer,
        ForeignKey(
            "likes.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
    UniqueConstraint("tweet_id", "like_id"),
)

tweets_media_association = Table(
    "tweets_media",
    Base.metadata,
    Column(
        "tweet_id",
        Integer,
        ForeignKey(
            "tweets.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
    Column(
        "media_id",
        Integer,
        ForeignKey(
            "media.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
)

user_tweets_association = Table(
    "user_tweets",
    Base.metadata,
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tweet_id",
        Integer,
        ForeignKey("tweets.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

subscription_table = Table(
    "subscription",
    Base.metadata,
    Column(
        "follower_id",
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
    Column(
        "followed_id",
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
)
