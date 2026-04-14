from pydantic import BaseModel
from typing import List
from datetime import datetime


class PostFeed(BaseModel):
    id: int
    title: str
    content: str
    authore: str
    created_at: datetime

    class Config:
        from_attributes = True


class CommentMeta(BaseModel):
    no_comment: int
    link: str


class FeedItem(BaseModel):
    post: PostFeed
    votes: int
    comment: CommentMeta

    class Config:
        from_attributes = True

class FeedResponse(BaseModel):
    data: List[FeedItem]
    pagination: dict
















