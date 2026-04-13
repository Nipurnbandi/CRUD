from pydantic import BaseModel


class FollowResponse(BaseModel):
    status: str
