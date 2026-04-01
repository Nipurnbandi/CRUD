from fastapi import APIRouter,Depends,HTTPException,status
from .. import models,schemas
from ..database import get_db
from sqlalchemy.orm import Session
from ..oauth2 import current_user

router=APIRouter(
    prefix="/comment",
    tags=["comment"]
)

@router.post("/{id}",response_model=schemas.Response_comment)
async def post_comment(id:int,request_model:schemas.Request_comment,db:Session=Depends(get_db),current_us=Depends(current_user)):
    
    check_comment=db.query(models.Post).filter(models.Post.id==id).first()

    if not check_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    data=models.Comment(
        post_id=id,
        user_id=current_us.id,
        content=request_model.content,
    )

    db.add(data)
    db.commit()
    db.refresh(data)

    return data
    

    
    



