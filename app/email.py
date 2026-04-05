
from email.message import EmailMessage
import aiosmtplib
from .config import settings


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
    reset_link = f"{settings.front_end_url}/reset-password?token={token}"

    subject = "Password Reset Request"

    plain_text = f"""
Hi {to_email},

You requested to reset your password.

Click the link below to reset it:
{reset_link}

If you did not request this, please ignore this email.
b
Thanks,
Your Team
"""

    await send_email(
        to_mail=to_email,
        subject=subject,
        plain_text=plain_text,
    )


import secrets
from datetime import datetime, timedelta

async def create_token():
    return secrets.token_urlsafe(32)

async def expire_time():
    expiry = datetime.utcnow() + timedelta(minutes=15)
    return  expiry
    
    