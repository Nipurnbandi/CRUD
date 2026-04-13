from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Post_users(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)


class Login_details(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_typ: str


class Token_data(BaseModel):
    id: Optional[int]


class UserResponse(BaseModel):
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class ForgetPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    new_password: str
