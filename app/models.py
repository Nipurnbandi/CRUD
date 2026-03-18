from .database import Base
from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__="post"
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    authore=Column(String,default="Unknown")
    published=Column(Boolean,server_default=text('true'),nullable=False)
    created_at=Column(TIMESTAMP,server_default=text('now()'),nullable=False)
    
class Users(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP,server_default=text('now()'),nullable=False)