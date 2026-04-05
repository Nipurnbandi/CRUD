from fastapi import Depends, APIRouter, HTTPException,BackgroundTasks,status
from ..database import get_db
from datetime import datetime
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
        token=utils.hash(token_),
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


@router.post("/reset_password")
async def reset_password(resetPassword:schemas.ResetPassword,db:Session=Depends(get_db)):

    query=db.query(models.PasswordResetToken).filter(models.PasswordResetToken.email==resetPassword.email).first()

    if not query or not utils.verify(resetPassword.token, query.token):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="expired or invalid token")
    
    if query.expires_at < datetime.utcnow():
        db.delete(query)
        db.commit()
        raise HTTPException(
        status_code=400,
        detail="Token expired"
    )


    user_query=db.query(models.Users).filter(models.Users.email==query.email).first()

    if not user_query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="expired or invalid token")
    
    user_query.password=utils.hash(resetPassword.new_password)
    db.delete(query)
    db.commit()
    return {"message":"Password reset successfullly"}
