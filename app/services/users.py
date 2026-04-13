from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models
from app.core import security


# CREATE USER
def create_user(db: Session, user_data):
    
    # Check if user exists
    existing_user = db.query(models.Users).filter(
        models.Users.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Password strength check
    if not security.is_password_strong(user_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide a strong password"
        )

    # Hash password
    hashed_password = security.hash(user_data.password)

    new_user = models.Users(
        email=user_data.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# GET USER BY ID
def get_user_by_id(db: Session, user_id: int):
    user = db.query(models.Users).filter(
        models.Users.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user