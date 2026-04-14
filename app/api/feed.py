from fastapi import APIRouter,Depends,Query,Request
from app.services import feed as service
from sqlalchemy.orm import Session
from .. import schemas
from ..core.database import get_db
from app.core.jwt import current_user
from app.services import feed as service
from app.schemas.feed import FeedResponse
from typing import List


router=APIRouter()


@router.get("/feed", response_model=FeedResponse)
def get_feed(request:Request,page:int=Query(1,ge=1),page_size:int=Query(3,ge=3),db: Session = Depends(get_db)):
    return service.get_feed(db,page,page_size,request)


