from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models


def toggle_follow(db: Session, current_user_id: int, target_user_id: int):
    
    if current_user_id == target_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot follow yourself"
        )

    existing = db.query(models.Followers).filter(
        models.Followers.current_user_id == current_user_id,
        models.Followers.follower_id == target_user_id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return {"status": "unfollowed"}

    new_follow = models.Followers(
        current_user_id=current_user_id,
        follower_id=target_user_id
    )
    db.add(new_follow)
    db.commit()

    return {"status": "followed"}


def get_followers(db: Session, user_id: int):
    
    followers = db.query(models.Followers).filter(
        models.Followers.follower_id == user_id
    ).all()

    return followers