
from pydantic import BaseModel,Field,EmailStr
from datetime import datetime
from typing import Optional

#### Request model #########Data from user->DB 
class Post_Base(BaseModel):
    title: str = Field(..., max_length=40, min_length=10)
    content: str = Field(..., min_length=40, max_length=10000)
    published: bool = Field(default=True)
    authore: str  = Field(default=None,min_length=2)
    

class Post_create(Post_Base):
    pass




class Post_update(BaseModel):
    title: str = Field(..., max_length=40, min_length=10)
    content:str= Field(...,max_length=10000, min_length=40 )




class Post_users(BaseModel):
    
    email:EmailStr
    password:str= Field(min_length=8, max_length=64)

class Login_details(BaseModel):
    email:EmailStr
    password:str=Field(min_length=8, max_length=64)

class Token(BaseModel):
    access_token:str
    token_typ:str

class Token_data(BaseModel):
    id:Optional[int]

#### Response Model ######Data from server->browser

class Response_read(BaseModel):
    title: str
    content: str
    
class PostWithVotes(BaseModel):
    post: Response_read
    votes: int

class Response_create(BaseModel):
    title: str 
    content: str
    published: bool 
    authore: str 
    created_at:datetime

    class Config:
        orm_mode=True

class Response_update(BaseModel):    
    title: str 
    content: str 
    published: bool 
    authore:str
    created_at:datetime

    class Config:
        orm_mode=True





class UserResponse(BaseModel):
    
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True  