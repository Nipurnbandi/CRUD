from fastapi import Depends, APIRouter, HTTPException,BackgroundTasks,status
from ..database import get_db
from datetime import datetime,timezone
from sqlalchemy.orm import Session
from .. import oauth2, models, email,utils,schemas

router = APIRouter()

@router.post("/reset_send_mail")
async def rest_password_send_mail(
    forget_password:schemas.ForgetPassword,
    background_task:BackgroundTasks,
    db: Session = Depends(get_db),
    
):
    token_ = email.create_token()
    
    user = db.query(models.Users).filter(models.Users.email == forget_password.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.query(models.PasswordResetToken).filter(models.PasswordResetToken.email == forget_password.email).delete()
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

    return {"message": "email sent"}



@router.post("/reset_password/")
async def reset_password(
    token: str,
    resetPassword: schemas.ResetPassword,
    db: Session = Depends(get_db)
):
    # find token
    query = db.query(models.PasswordResetToken).filter(
        models.PasswordResetToken.token == token
    ).first()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="expired or invalid token"
        )

    # check expiry
    if query.expires_at < datetime.now(timezone.utc):
        db.delete(query)
        db.commit()
        raise HTTPException(
            status_code=400,
            detail="Token expired"
        )

    # get user
    user = db.query(models.Users).filter(
        models.Users.email == query.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="invalid request"
        )

    if not utils.is_password_strong(resetPassword.new_password):
         raise HTTPException(status_code=400, detail="Weak password")

    # update password
    user.password = utils.hash(resetPassword.new_password)

    # delete token
    db.delete(query)
    db.commit()

    return {"message": "Password reset successfully"}



















