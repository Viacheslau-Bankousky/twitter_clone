"""Initial migration.

Revision ID: 51ec19b8c4cb
Revises: -
Create Date: 2024-05-04 19:23:56.337420

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

USER_ID: str = "user_id"
LIKE_ID: str = "like_id"
CASCADE: str = "CASCADE"
ID: str = "id"
TWEET_ID: str = "tweet_id"
USERS_ID: str = "users.id"

revision: str = "51ec19b8c4cb"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:  # noqa: WPS213
    """
    Drop existing tables to upgrade the database.

    This function, when run, will remove a series of tables from
    the current database.
    """
    op.drop_table("tweets_likes")
    op.drop_table("user_likes")
    op.drop_table("user_tweets")
    op.drop_table("subscription")
    op.drop_table("users")
    op.drop_table("likes")
    op.drop_table("tweets_media")
    op.drop_table("tweets")
    op.drop_table("media")


def downgrade() -> None:  # noqa: WPS213
    """
    Create tables to downgrade the database.

    This function will roll back the actions of the upgrade() function,
    recreating the tables that were deleted.
    """
    op.create_table(
        "user_likes",
        sa.Column(
            "user_id", sa.INTEGER(), autoincrement=False, nullable=False,
        ),
        sa.Column(
            "like_id", sa.INTEGER(), autoincrement=False, nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["like_id"],
            ["likes.id"],
            name="user_likes_like_id_fkey",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="user_likes_user_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("user_id", "like_id", name="user_likes_pkey"),
    )
    op.create_table(
        "media",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('media_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("file", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="media_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "tweets",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('tweets_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "tweet_data", sa.VARCHAR(), autoincrement=False, nullable=True,
        ),
        sa.PrimaryKeyConstraint("id", name="tweets_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "user_tweets",
        sa.Column(
            "user_id", sa.INTEGER(), autoincrement=False, nullable=False,
        ),
        sa.Column(
            "tweet_id", sa.INTEGER(), autoincrement=False, nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["tweet_id"],
            ["tweets.id"],
            name="user_tweets_tweet_id_fkey",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="user_tweets_user_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "user_id", "tweet_id", name="user_tweets_pkey",
        ),
    )
    op.create_table(
        "subscription",
        sa.Column(
            "follower_id", sa.INTEGER(), autoincrement=False, nullable=False,
        ),
        sa.Column(
            "followed_id", sa.INTEGER(), autoincrement=False, nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["followed_id"],
            ["users.id"],
            name="subscription_followed_id_fkey",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["follower_id"],
            ["users.id"],
            name="subscription_follower_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "follower_id", "followed_id", name="subscription_pkey",
        ),
    )
    op.create_table(
        "tweets_media",
        sa.Column(
            "tweet_id", sa.INTEGER(), autoincrement=False, nullable=False,
        ),
        sa.Column(
            "media_id", sa.INTEGER(), autoincrement=False, nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["media_id"],
            ["media.id"],
            name="tweets_media_media_id_fkey",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["tweet_id"],
            ["tweets.id"],
            name="tweets_media_tweet_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "tweet_id", "media_id", name="tweets_media_pkey",
        ),
    )
    op.create_table(
        "likes",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('likes_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="likes_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "users",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "api_key", sa.VARCHAR(), autoincrement=False, nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
    )
    op.create_index("ix_users_api_key", "users", ["api_key"], unique=True)
    op.create_table(
        "tweets_likes",
        sa.Column(
            "tweet_id", sa.INTEGER(), autoincrement=False, nullable=False,
        ),
        sa.Column(
            "like_id", sa.INTEGER(), autoincrement=False, nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["like_id"],
            ["likes.id"],
            name="tweets_likes_like_id_fkey",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["tweet_id"],
            ["tweets.id"],
            name="tweets_likes_tweet_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "tweet_id", "like_id", name="tweets_likes_pkey",
        ),
    )
