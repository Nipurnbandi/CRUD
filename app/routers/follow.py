from fastapi import Depends,APIRouter,HTTPException,status
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas,oauth2,models


router=APIRouter()


@router.post("/follow/{id}")
async def follow(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.current_user)
):

    # Check if already followed
    existing = db.query(models.Followers).filter(
        models.Followers.current_user_id == current_user.id,
        models.Followers.follower_id == id
    ).first()

    if existing:
        # Unfollow
        db.delete(existing)
        db.commit()
        return {"status": "unfollowed"}

    else:
        #follow
        data = models.Followers(
            current_user_id=current_user.id,
            follower_id=id
        )
        db.add(data)
        db.commit()
        return {"status": "followed"}










   
@router.post("/see_followers/{id}")
async def see_followers(id:int,db:Session=Depends(get_db),current_user=Depends(oauth2.current_user)):
    pass
