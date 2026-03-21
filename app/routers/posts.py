from .. import models,schemas
from ..database import get_db
from sqlalchemy.orm import Session
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
@router.get("/{id}",status_code=status.HTTP_201_CREATED,response_model=schemas.Response_read)
async def read_post(id:int,db: Session = Depends(get_db)):
    data=db.query(models.Post).filter(models.Post.id==id).first()
    if not data:
        raise HTTPException(status_code=404,detail=f"not found given {id}")
    return data





#create
@router.post("",response_model=schemas.Response_create)
async def create_post(post_create: schemas.Post_create,db:Session=Depends(get_db)):
    data=models.Post(title=post_create.title,content=post_create.content,authore=post_create.authore,published=post_create.published)
    db.add(data)       
    db.commit()            
    db.refresh(data)
    return data





#deletion
@router.delete("/{id}")
async def delete_post(id: int,db:Session=Depends(get_db)):
    deleted_post=db.query(models.Post).filter(models.Post.id==id)
    if not deleted_post.first():
        raise HTTPException(status_code=404, detail="Post does not exist")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return {
        "message": "Post deleted successfully",
        "deleted_post": deleted_post.first()
    }





#Update
@router.put("/{id}",response_model=schemas.Response_update)
async def update(id: int, post_update: schemas.Post_update,db:Session=Depends(get_db)):
    post_querry=db.query(models.Post).filter(models.Post.id==id)


    if not  post_querry.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    
    post_querry.update(post_update.model_dump(),synchronize_session=False)
    db.commit()
    return post_querry.first()