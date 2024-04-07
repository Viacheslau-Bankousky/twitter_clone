"""
A Pydantic module with several models for managing tweets and media.

These models help in constructing standardized requests and responses
across the tweet-related operations in the application.

Classes:
--------
Tweet:
    A model defining the structure of a Tweet.

TweetResponse:
    A model defining the response structure after performing operations
    related to a single tweet.

AllTweetsResponse:
    A model defining the response structure after retrieving all tweets.

TweetRequest:
    A model defining the request structure for creating a tweet.

MediaResponse:
    A model defining the response structure after performing operations
    related to media.

Modules:
--------
typing: Supports type hints.
pydantic: A data validation and settings management library using python
type annotations.
application.schemas.basic_schemas: Contains basic response schemas.
application.schemas.user_schemas: Contains user-related schemas.
"""

from typing import List, Optional

from pydantic import BaseModel, Field

from application.schemas.basic_schemas import BasicSuccessResponse
from application.schemas.user_schemas import UserConnections


class Tweet(BaseModel):
    """
    Represents a Tweet in the application.

    Fields:
    -------
    id (int):
        Unique ID of this Tweet.
    content (str):
        The content of this Tweet.
    attachments (Optional[List[str]]):
        Possible attachments in this Tweet.
    author (UserConnections):
        The author of this Tweet.
    likes (Optional[List[UserConnections]]):
        Users who liked this Tweet.
    """

    id: int = Field(..., description="Tweet ID")
    content: str = Field(..., description="Tweet content")  # noqa: WPS110
    attachments: Optional[List[str]] = Field(
        ...,
        description="Attachments of the tweet if available",
    )
    author: UserConnections = Field(..., description="Author of the tweet")
    likes: Optional[List[UserConnections]] = Field(
        ...,
        description="Likes for the tweet",
    )


class TweetResponse(BasicSuccessResponse):
    """
    The response model for performing operations related to a single tweet.

    Inherits from BasicSuccessResponse and adds the 'tweet_id'.

    Fields:
    -------
    tweet_id (int):
        Unique ID of the new or updated tweet.
    """

    tweet_id: int = Field(..., description="ID of the new tweet")


class AllTweetsResponse(BasicSuccessResponse):
    """
    The response model when retrieving all tweets.

    Inherits from BasicSuccessResponse and includes a list of 'tweets'.

    Fields:
    -------
    tweets (Optional[List[Tweet]]):
        A list of all tweets in the application.
    """

    tweets: Optional[List[Tweet]] = Field(..., description="List of tweets")


class TweetRequest(BaseModel):
    """
    The request model for creating a tweet.

    Fields:
    -------
    tweet_data (str):
        Content for the new tweet.
    tweet_media_ids (Optional[List[int]]):
        Ids of media files associated with this tweet.
    """

    tweet_data: str = Field(..., description="Tweet data")
    tweet_media_ids: Optional[List[int]] = Field(
        None,
        description="Tweet media ids",
    )


class MediaResponse(BasicSuccessResponse):
    """
    The response model when performing operations related to media.

    Inherits from BasicSuccessResponse and adds the 'media_id'.

    Fields:
    -------
    media_id (int):
        Unique ID of the new media file.
    """

    media_id: int = Field(..., description="ID of the media file")
