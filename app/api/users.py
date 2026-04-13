from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy.orm import Session

from app.core import email
from app.core.database import get_db
from app.schemas.auth import Post_users, UserResponse
from app.services import users as service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# REGISTER USER
@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(
    post_users: Post_users,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    new_user = service.create_user(db=db, user_data=post_users)

    # Send email (kept in API layer because it's side-effect / async task trigger)
    background_tasks.add_task(
        email.send_email_verification_email,
        new_user.email
    )

    return new_user


# GET USER DETAILS
@router.get("/{id}", response_model=UserResponse)
async def users_details(
    id: int,
    db: Session = Depends(get_db)
):
    return service.get_user_by_id(db=db, user_id=id)