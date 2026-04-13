from fastapi import APIRouter, Depends, Request, Header, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.database import get_db
from app.schemas.auth import ForgetPassword, ResetPassword
from app.services import auth as service

router = APIRouter(tags=["authentication"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/login")
@limiter.limit("10/minute")
@limiter.limit("3/second")
async def user_login(
    request: Request,
    login_details: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    access, refresh = service.login_user(db, login_details)

    return {
        "status": "login successful",
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }


@router.post("/refresh")
async def refresh_token(
    refresh_token: str = Header(..., alias="X-Refresh-Token"),
    db: Session = Depends(get_db)
):
    access, refresh = service.refresh_user_token(db, refresh_token)

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(
    refresh_token: str = Header(..., alias="X-Refresh-Token"),
    db: Session = Depends(get_db)
):
    service.logout_user(db, refresh_token)
    return {"message": "Logged out successfully"}


@router.post("/reset_send_mail")
async def rest_password_send_mail(
    forget_password: ForgetPassword,
    background_task: BackgroundTasks,
    db: Session = Depends(get_db),
):
    service.send_reset_email(db, forget_password, background_task)
    return {"message": "email sent"}


@router.post("/reset_password/")
async def reset_password(
    token: str,
    resetPassword: ResetPassword,
    db: Session = Depends(get_db)
):
    service.reset_user_password(db, token, resetPassword)
    return {"message": "Password reset successfully"}


@router.post("/verify_email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    service.verify_user_email(db, token)
    return {"message": "Email verified successfully"}