from fastapi import  HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,oauth2
from ..database import get_db

router=APIRouter()

@router.post("/vote/{post_id}")
async def vote(
    post_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.current_user)
):
    # check if already liked
    existing_vote = db.query(models.Votes).filter(
        models.Votes.post_id == post_id,
        models.Votes.user_id == current_user.id
    ).first()

    if existing_vote:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already liked this post"
        )

    new_vote = models.Votes(
        user_id=current_user.id,
        post_id=post_id
    )

    db.add(new_vote)
    db.commit()

    return {"response": "liked"}
