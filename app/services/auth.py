from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone, timedelta
from ..core import email
from .. import models 
from app.core import jwt,config,security
import secrets


def create_refresh_token():
    return secrets.token_urlsafe(64)


def normalize_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def login_user(db: Session, login_details):
    user = db.query(models.Users).filter(
        models.Users.email == login_details.username
    ).first()

    if not user or not security.verify(login_details.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    access_token = jwt.create_access_token(data={"user_id": user.id})
    refresh_token = create_refresh_token()

    try:
        db.add(models.RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.now(timezone.utc) + timedelta(
                days=config.settings.refresh_token_expire_days
            )
        ))
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Something went wrong")

    return access_token, refresh_token


def refresh_user_token(db: Session, refresh_token: str):
    token_data = db.query(models.RefreshToken).filter(
        models.RefreshToken.token == refresh_token
    ).first()

    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if normalize_utc(token_data.expires_at) < datetime.now(timezone.utc):
        try:
            db.delete(token_data)
            db.commit()
        except SQLAlchemyError:
            db.rollback()
        raise HTTPException(status_code=401, detail="Refresh token expired")

    user_id = token_data.user_id
    new_access_token = jwt.create_access_token(data={"user_id": user_id})
    new_refresh_token = create_refresh_token()

    try:
        db.delete(token_data)
        db.add(models.RefreshToken(
            user_id=user_id,
            token=new_refresh_token,
            expires_at=datetime.now(timezone.utc) + timedelta(
                days=config.settings.refresh_token_expire_days
            )
        ))
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Something went wrong")

    return new_access_token, new_refresh_token


def logout_user(db: Session, refresh_token: str):
    token_data = db.query(models.RefreshToken).filter(
        models.RefreshToken.token == refresh_token
    ).first()

    if token_data:
        try:
            db.delete(token_data)
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Something went wrong")


def send_reset_email(db: Session, forget_password, background_task):
    token_ = email.create_token()

    user = db.query(models.Users).filter(
        models.Users.email == forget_password.email
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.query(models.PasswordResetToken).filter(
        models.PasswordResetToken.email == forget_password.email
    ).delete()
    db.commit()

    reset_entry = models.PasswordResetToken(
        id=user.id,
        email=user.email,
        token=token_,
        expires_at=email.expire_time()
    )

    db.add(reset_entry)
    db.commit()

    background_task.add_task(
        email.send_password_reset_email,
        to_email=user.email,
        token=token_,
    )


def reset_user_password(db: Session, token: str, resetPassword):
    query = db.query(models.PasswordResetToken).filter(
        models.PasswordResetToken.token == token
    ).first()

    if not query:
        raise HTTPException(status_code=400, detail="expired or invalid token")

    if query.expires_at < datetime.now(timezone.utc):
        db.delete(query)
        db.commit()
        raise HTTPException(status_code=400, detail="Token expired")

    user = db.query(models.Users).filter(
        models.Users.email == query.email
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="invalid request")

    if not security.is_password_strong(resetPassword.new_password):
        raise HTTPException(status_code=400, detail="Weak password")

    user.password = security.hash(resetPassword.new_password)

    db.delete(query)
    db.commit()


def verify_user_email(db: Session, token: str):
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

    user = db.query(models.Users).filter(
        models.Users.id == check_token.id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.verified = True
    db.delete(check_token)
    db.commit()