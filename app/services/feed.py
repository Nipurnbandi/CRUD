from sqlalchemy.orm import Session, joinedload
from .. import models
from fastapi import Request


def get_feed(db: Session,page,page_size,request):
    limit=page_size
    offset=(page-1)*limit

    total=db.query(models.Post).count()
    base_url=str(request.url).split('?')[0]

    if offset+limit <total:
        next_url=f"{base_url}?page={page+1}&page_size={limit}"
    else:
        next_url=None
    
    if page>1:
        prev_url=f"{base_url}?page={page-1}&page_size={limit}"
    else:
        prev_url=None
    
    posts = (
        db.query(models.Post)
        .options(
            joinedload(models.Post.comments),
            joinedload(models.Post.votes),
            joinedload(models.Post.user)
        ).offset(offset).limit(limit).all()
    )

    result = []

    for p in posts:
        result.append({
            "post": {
                "id": p.id,
                "title": p.title,
                "content": p.content,
                "authore": p.user.email,
                "created_at": p.created_at
            },
            "votes": len(p.votes),
            "comment": {
                "no_comment": len(p.comments),
                "link": f"http://127.0.0.1:8000/comment/{p.id}"
            }
        })

    return {
        "data":result,
        "pagination":{"next":next_url,
                      "prev":prev_url}
    }