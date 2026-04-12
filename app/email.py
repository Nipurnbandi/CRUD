
from email.message import EmailMessage
import aiosmtplib
from . import models
from fastapi import HTTPException
from .config import settings
import secrets
from .database import SessionLocal
from datetime import datetime, timedelta,timezone
from sqlalchemy.orm import Session

async def send_email(
    to_mail: str,
    subject: str,
    plain_text: str,
):
    message = EmailMessage()
    message["From"] = settings.mail_from
    message["To"] = to_mail
    message["Subject"] = subject
    message.set_content(plain_text)

    await aiosmtplib.send(
        message,
        hostname=settings.mail_server,
        port=settings.mail_port,
        username=settings.mail_username if settings.mail_username else None,
        password=settings.mail_password,
        start_tls=settings.mail_use_tls,
    )


async def send_password_reset_email(to_email: str,token: str):
    reset_link = f"{settings.front_end_url}/reset_password?token={token}"

    subject = "Password Reset Request"

    plain_text = f"""
Hi {to_email},

You requested to reset your password.

Click the link below to reset it:
{reset_link}

If you did not request this, please ignore this email.

Thanks,
Your Team
"""
    
    await send_email(
        to_mail=to_email,
        subject=subject,
        plain_text=plain_text,
    )


def create_token():
    return secrets.token_urlsafe(32)


def expire_time():
    expiry = datetime.now(timezone.utc) + timedelta(minutes=15)
    return  expiry




async def send_email_verification_email(to_email: str):
    db = SessionLocal()
    try:
        user = db.query(models.Users).filter(models.Users.email == to_email).first()

        if not user:
            return  

        token_ = create_token()

        data = models.EmailVerify(
            id=user.id,
            email=to_email,
            token=token_,
            expires_at=expire_time()
        )

        db.add(data)
        db.commit()

        verify_link = f"http://127.0.0.1:8000/users/verify_email?token={token_}"

        await send_email(
            to_mail=to_email,
            subject="Verify your email",
            plain_text=f"Click here:\n{verify_link}"
        )

    finally:
        db.close()   

























































    