from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from .. import models


# GET ALL POSTS
def get_all_posts(db: Session):
    return db.query(models.Post).all()


# GET SINGLE POST WITH VOTES + COMMENTS
def get_post_by_id(db: Session, post_id: int):
    data = db.query(
        models.Post,
        func.count(models.Votes.post_id).label("votes")
    ).outerjoin(
        models.Votes, models.Votes.post_id == models.Post.id
    ).group_by(
        models.Post.id
    ).filter(
        models.Post.id == post_id
    ).first()

    if not data:
        raise HTTPException(status_code=404, detail="Post not found")

    comments = db.query(models.Comment).filter(
        models.Comment.post_id == post_id
    ).all()

    return {
        "post": data[0],
        "votes": data[1],
        "comment": comments
    }


# CREATE POST
def create_post(db: Session, post_data, user_id: int):
    new_post = models.Post(
        title=post_data.title,
        content=post_data.content,
        authore=post_data.authore,
        published=post_data.published,
        user_id=user_id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# DELETE POST
def delete_post(db: Session, post_id: int, user_id: int):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=404, detail="Post does not exist")

    if post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this post"
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Post deleted successfully"}


# UPDATE POST
def update_post(db: Session, post_id: int, post_data, user_id: int):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist"
        )

    if post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update this post"
        )

    post_query.update(post_data.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()