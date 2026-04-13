from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core import jwt
from app.services import vote as service

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/{post_id}")
async def vote(
    post_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(jwt.current_user)
):
    return service.toggle_vote(
        db=db,
        post_id=post_id,
        user_id=current_user.id
    )