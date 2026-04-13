from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models


def create_comment(db: Session, post_id: int, user_id: int, content: str):
    
    check_post = db.query(models.Post).filter(
        models.Post.id == post_id
    ).first()

    if not check_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    data = models.Comment(
        post_id=post_id,
        user_id=user_id,
        content=content,
    )

    db.add(data)
    db.commit()
    db.refresh(data)

    return data