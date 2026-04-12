from .. import models,schemas,utils
from datetime import datetime,timezone
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from fastapi import  HTTPException,status,Depends,APIRouter,BackgroundTasks
from .. import email

router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

#register
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse,)
async def create_user(post_users: schemas.Post_users,background_tasks: BackgroundTasks,db: Session = Depends(get_db)):

    # Check if user already exists
    existing_user = db.query(models.Users).filter(models.Users.email == post_users.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    if not utils.is_password_strong(post_users.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="please provide strong password")

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

    background_tasks.add_task(
        email.send_email_verification_email,
        new_user.email
    )

    return new_user


#users details
@router.get("/{id}",response_model=schemas.UserResponse)
async def users_details(id:int,db:Session=Depends(get_db)):
    data=db.query(models.Users).filter(models.Users.id==id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="data not found")
    
    return data




@router.post("/verify_email")
async def verify_email(token: str, db: Session = Depends(get_db)):

    
    check_token = db.query(models.EmailVerify).filter(
        models.EmailVerify.token == token
    ).first()

    if not check_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )

    
    if check_token.expires_at < datetime.now(timezone.utc):
        db.delete(check_token)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token expired"
        )

    # get user
    user = db.query(models.Users).filter(
        models.Users.id == check_token.id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # mark verified
    user.verified = True

    # delete token (one-time use)
    db.delete(check_token)

    db.commit()

    return {"message": "Email verified successfully"}











