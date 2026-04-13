from datetime import datetime

from pydantic import BaseModel


class Request_comment(BaseModel):
    content: str


class CommentResponse(BaseModel):
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class Response_comment(BaseModel):
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
