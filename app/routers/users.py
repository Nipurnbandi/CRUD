from .. import models,schemas
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from fastapi import  HTTPException,status,Depends,APIRouter

router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

#login users
@router.post("",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
async def create_user(post_users:schemas.Post_users,db:Session=Depends(get_db)):
    new_user = models.Users(email=post_users.email,password=post_users.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user




#users details
@router.get("/{id}",response_model=schemas.UserResponse)
async def users_details(id:int,db:Session=Depends(get_db)):
    data=db.query(models.Users).filter(models.Users.id==id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="data not found")
    
    return data