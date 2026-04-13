from fastapi import APIRouter, Depends, HTTPException, Request, status, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone, timedelta
from slowapi import Limiter
from slowapi.util import get_remote_address
from ..database import get_db
from .. import models, oauth2, utils, config
import secrets

router = APIRouter(tags=["authentication"])
limiter = Limiter(key_func=get_remote_address)

def create_refresh_token():
    return secrets.token_urlsafe(64)

def normalize_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


@router.post("/login")
@limiter.limit("10/minute")
@limiter.limit("3/second")
async def user_login(
    request: Request,
    login_details: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.Users).filter(
        models.Users.email == login_details.username
    ).first()

    if not user or not utils.verify(login_details.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
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

    return {
        "status": "login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
async def refresh_token(
    refresh_token: str = Header(..., alias="X-Refresh-Token"),
    db: Session = Depends(get_db)
):
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
    new_access_token = oauth2.create_access_token(data={"user_id": user_id})
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

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(
    refresh_token: str = Header(..., alias="X-Refresh-Token"),
    db: Session = Depends(get_db)
):
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

    return {"message": "Logged out successfully"}