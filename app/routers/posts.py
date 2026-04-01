from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from fastapi import  HTTPException,status,Depends,APIRouter

router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


#read all 
@router.get("",response_model=List[schemas.Response_read])
async def all(db: Session = Depends(get_db)):
    data=db.query(models.Post).all()
    return data


#acess/read
@router.get("/{id}", response_model=schemas.PostWithVotes)
def read_post(id: int, db: Session = Depends(get_db)):
    data = db.query(
        models.Post,
        func.count(models.Votes.post_id).label("votes")
    ).outerjoin(
        models.Votes, models.Votes.post_id == models.Post.id
    ).group_by(
        models.Post.id
    ).filter(
        models.Post.id == id
    ).first()

    all_comment=db.query(models.Comment).filter(models.Comment.post_id==id).all()

    if not data:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "post": data[0],  
        "votes": data[1],
        "comment":all_comment
    }


#create
@router.post("", response_model=schemas.Response_create)
async def create_post(
    post_create: schemas.Post_create,
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.current_user)
):
    data = models.Post(
        title=post_create.title,
        content=post_create.content,
        authore=post_create.authore,
        published=post_create.published,
        user_id=current_user.id
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


#deletion
@router.delete("/{id}")
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=404, detail="Post does not exist")

    
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this post"
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Post deleted successfully"}


#Update
@router.put("/{id}", response_model=schemas.Response_update)
async def update(
    id: int,
    post_update: schemas.Post_update,
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.current_user)
    ):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # Check if post exists
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist"
        )

    # Authorization check
    if post.user_id != user_id.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update this post"
        )

    post_query.update(post_update.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()