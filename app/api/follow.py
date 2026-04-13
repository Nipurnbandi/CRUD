from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core import jwt
from app.services import follow as service

router = APIRouter(
    prefix="/follow",
    tags=["Follow"]
)


@router.post("/{id}")
async def follow_user(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(jwt.current_user)
):
    return service.toggle_follow(
        db=db,
        current_user_id=current_user.id,
        target_user_id=id
    )


@router.get("/followers/{id}")
async def see_followers(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(jwt.current_user)
):
    return service.get_followers(db=db, user_id=id)