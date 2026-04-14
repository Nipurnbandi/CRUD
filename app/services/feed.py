from sqlalchemy.orm import Session, joinedload
from fastapi import Request
from .. import models


def get_feed(db: Session, page: int, page_size: int, request: Request):

    limit = page_size
    offset = (page - 1) * limit

    total = db.query(models.Post).count()

    base_url = f"{request.url.scheme}://{request.url.netloc}{request.url.path}"

    next_url = None
    prev_url = None

    if offset + limit < total:
        next_url = f"{base_url}?page={page + 1}&page_size={limit}"

    if page > 1:
        prev_url = f"{base_url}?page={page - 1}&page_size={limit}"

    posts = (
        db.query(models.Post)
        .options(
            joinedload(models.Post.comments),
            joinedload(models.Post.votes),
            joinedload(models.Post.user)
        )
        .offset(offset)
        .limit(limit)
        .all()
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
            "votes": {"no_votes":len(p.votes),
                      "vote_post":f" http://127.0.0.1:8000/vote/{p.id}"},
            "comment": {
                "no_comment": len(p.comments),
                "link": f"{base_url}/comment/{p.id}"
            }
        })

    return {
        "data": result,
        "pagination": {
            "total": total,
            "page": page,
            "page_size": limit,
            "next": next_url,
            "prev": prev_url
        }
    }