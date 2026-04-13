from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from app.core import jwt
from app.schemas.posts import (
    PostWithVotes,
    Post_create,
    Post_update,
    Response_create,
    Response_read,
    Response_update,
)
from app.services import posts as service

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# GET ALL
@router.get("", response_model=List[Response_read])
async def all_posts(db: Session = Depends(get_db)):
    return service.get_all_posts(db)


# GET SINGLE
@router.get("/{id}", response_model=PostWithVotes)
async def read_post(id: int, db: Session = Depends(get_db)):
    return service.get_post_by_id(db, id)


# CREATE
@router.post("", response_model=Response_create)
async def create_post(
    post_create: Post_create,
    db: Session = Depends(get_db),
    current_user = Depends(jwt.current_user)
):
    return service.create_post(
        db=db,
        post_data=post_create,
        user_id=current_user.id
    )


# DELETE
@router.delete("/{id}")
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(jwt.current_user)
):
    return service.delete_post(
        db=db,
        post_id=id,
        user_id=current_user.id
    )


# UPDATE
@router.put("/{id}", response_model=Response_update)
async def update_post(
    id: int,
    post_update: Post_update,
    db: Session = Depends(get_db),
    current_user = Depends(jwt.current_user)
):
    return service.update_post(
        db=db,
        post_id=id,
        post_data=post_update,
        user_id=current_user.id
    )