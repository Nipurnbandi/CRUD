from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.comment import Request_comment, Response_comment
from ..core.database import get_db
from app.core.jwt import current_user
from app.services import comment as service

router = APIRouter(
    prefix="/comment",
    tags=["comment"]
)


@router.post("/{id}", response_model=Response_comment)
async def post_comment(
    id: int,
    request_model: Request_comment,
    db: Session = Depends(get_db),
    current_us = Depends(current_user)
):
    
    data = service.create_comment(
        db=db,
        post_id=id,
        user_id=current_us.id,
        content=request_model.content
    )

    return data

from app.core.jwt import current_user