from jose import jwt,JWTError,ExpiredSignatureError
import datetime 
from . import schemas
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from . import models
from . import config

oauth_schema=OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = config.settings.refresh_token_expire_minutes

expired_tokens=set()

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.datetime.utcnow()+datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data:dict):
    to_encode=data.copy()
    expire=datetime.datetime.utcnow()+datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
                    
        if user_id is None or token in expired_tokens:
            raise credential_exception

        token_data = schemas.Token_data(id=user_id)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token has expired, please login again",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except JWTError:
        raise credential_exception

    return token_data


def current_user(
    token: str = Depends(oauth_schema),
    db: Session = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="couldn't validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credential_exception)

    user = db.query(models.Users).filter(models.Users.id == token_data.id).first()

    if user is None:
        raise credential_exception

    return user 


def expire_token(token: str = Depends(oauth_schema),current_user=Depends(current_user)):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token already expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except  JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expired_tokens.add(token)

    return {"message": "Logged out successfully"}




























    
