from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from .. import models


def toggle_vote(db: Session, post_id: int, user_id: int):

    # Check post exists
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_vote = models.Votes(
        post_id=post_id,
        user_id=user_id
    )

    try:
        db.add(new_vote)
        db.commit()
        return {"data": "liked"}

    except IntegrityError:
        db.rollback()

        db.query(models.Votes).filter(
            models.Votes.post_id == post_id,
            models.Votes.user_id == user_id
        ).delete(synchronize_session=False)

        db.commit()
        return {"data": "unliked"}