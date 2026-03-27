from fastapi import  HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models,schemas,oauth2
from ..database import get_db

router=APIRouter()

@router.post("/vote/{post_id}")
async def vote(
    post_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.current_user)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_vote = models.Votes(
        post_id=post_id,
        user_id=current_user.id
    )

    try:
        # ✅ Try to LIKE
        db.add(new_vote)
        db.commit()
        return {"data": "liked"}

    except IntegrityError:
        db.rollback()

        # ❌ Already exists → UNLIKE
        db.query(models.Votes).filter(
            models.Votes.post_id == post_id,
            models.Votes.user_id == current_user.id
        ).delete(synchronize_session=False)

        db.commit()
        return {"data": "unliked"}




    









    





    
