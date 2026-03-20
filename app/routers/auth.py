from fastapi import  HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas
from ..database import get_db

router=APIRouter(
    tags=["authentication"]
)

@router.post("/login")
async def user_login(login_details:schemas.Login_details,db:Session=Depends(get_db)):
    data=db.query(models.Users).filter(models.Users.email==login_details.email).first()

    if not data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="credential not found")

    if not login_details.password==data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="credential not found")

    return {
        "data":"login successful"
    }