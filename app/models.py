from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,DateTime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from typing import Optional

class Post(Base):
    __tablename__="post"
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    authore = Column(String, nullable=True, default="Unknown")
    published=Column(Boolean,server_default=text('true'),nullable=False)
    created_at=Column(TIMESTAMP,server_default=text('now()'),nullable=False)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)


class Users(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    verified=Column(Boolean, server_default=text("false"))
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP,server_default=text('now()'),nullable=False)


class Votes(Base):
    __tablename__="votes"
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True,nullable=False)
    post_id=Column(Integer,ForeignKey("post.id",ondelete="CASCADE"),primary_key=True,nullable=False,)


class Comment(Base):
    __tablename__="comment"
    id=Column(Integer,primary_key=True,nullable=False)
    post_id=Column(Integer,ForeignKey("post.id",ondelete="CASCADE"),nullable=False)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    content=Column(String,nullable=False)
    created_at=Column(TIMESTAMP,server_default=text('now()'),nullable=False)


class Followers(Base):
    __tablename__="followers"
    current_user_id=Column(Integer,primary_key=True,nullable=False)
    follower_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True,nullable=False)
    created_at=Column(TIMESTAMP,server_default=text('now()'),nullable=False)


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True)
    email = Column(String, index=True)
    token = Column(String, unique=True)
    expires_at = Column(DateTime(timezone=True))

class EmailVerify(Base):
    __tablename__ = "email_verify"
    id = Column(Integer, primary_key=True)
    email = Column(String, index=True)
    token = Column(String, unique=True)
    expires_at = Column(DateTime(timezone=True))    
