from jose import JWTError,jwt
import datetime 
from . import schemas
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer

oauth_schema=OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1




def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.datetime.utcnow()+datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token:str,credential_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id=payload.get("user_id")

        if not id:
            raise credential_exception
    
        token_data=schemas.Token_data(id=id)

    except JWTError :
        raise credential_exception
    
    return token_data

def current_user(token: str=Depends(oauth_schema)):
    credential_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could'nt find credential",
        headers={"WWW-Authenticate":"Bearer"})
    
    return verify_access_token(token,credential_exception)