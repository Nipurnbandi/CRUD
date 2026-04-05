from fastapi import Depends, APIRouter, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import oauth2, models, email

router = APIRouter()

@router.post("/reset_send_mail")
async def rest_password_send_mail(
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.current_user)
):
    token = await email.create_token()

    user = db.query(models.Users).filter(models.Users.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    
    reset_entry = models.PasswordResetToken(
        email=user.email,
        token=token,
        expires_at=await email.expire_time()
    )

    db.add(reset_entry)
    db.commit()

    await email.send_password_reset_email(user.email, token)

    return {"message": "Reset email sent"}