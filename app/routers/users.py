from .. import models,schemas,utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from fastapi import  HTTPException,status,Depends,APIRouter

router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

#register
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(post_users: schemas.Post_users, db: Session = Depends(get_db)):

    # Check if user already exists
    existing_user = db.query(models.Users).filter(models.Users.email == post_users.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )


    #hashing of password
    hashed_password=utils.hash(post_users.password)

    # Create new user
    new_user = models.Users(
        email=post_users.email,
        password=hashed_password
    )

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