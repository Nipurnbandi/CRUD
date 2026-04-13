from pydantic import BaseModel


class VoteResponse(BaseModel):
    data: str
