from fastapi import  HTTPException,status,Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models,schemas,oauth2,utils
from ..database import get_db
from ..oauth2 import expire_token

router=APIRouter(
    tags=["authentication"]
) 

@router.post("/login")
async def user_login(login_details:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    data=db.query(models.Users).filter(models.Users.email==login_details.username).first()

    if not data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="credential not found")
    
    if not utils.verify(login_details.password,data.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="credential not found")
    access_token=oauth2.create_access_token(data={"user_id":data.id})

    return {
        "access_token":access_token,
        "token_type":"bearer"
    }


@router.post("/logout")
async def logout(result = Depends(oauth2.expire_token)):
    return result
