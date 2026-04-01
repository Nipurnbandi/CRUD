from fastapi import  HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models,oauth2
from ..database import get_db

router=APIRouter(
    prefix="/vote",
    tags=["vote"]
)



@router.post("/{post_id}")
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
        
        db.add(new_vote)
        db.commit()
        return {"data": "liked"}

    except IntegrityError:
        db.rollback()

        
        db.query(models.Votes).filter(
            models.Votes.post_id == post_id,
            models.Votes.user_id == current_user.id
        ).delete(synchronize_session=False)

        db.commit()
        return {"data": "unliked"}




    









    





    
