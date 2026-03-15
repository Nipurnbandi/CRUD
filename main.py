from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class Post_model(BaseModel):
    title: str = Field(..., max_length=40, min_length=10)
    content: str = Field(..., min_length=40, max_length=10000)
    published: bool = Field(default=True)
    authore: str  = Field(min_length=2)

post = {
1:{
"title":"Learning FastAPI properly",
"content":"This is a long content explaining how FastAPI works in detail.",
"published":True,
"authore":"Alex"
},
2:{
"title":"Understanding APIs in depth",
"content":"This article explains APIs and how backend systems work.",
"published":True,
"authore":"John"
},
3:{
"title":"Backend development basics",
"content":"Backend development includes databases, APIs and servers.",
"published":True,
"authore":"Mike"
}
}

#acess/read

@app.get("/home/{id}")
async def read_post(id:int):
    users_post_data = post.get(id)
    if not users_post_data:
        raise HTTPException(status_code=404)
    return users_post_data



#create


@app.post("/create_post")
async def create_post(post_model: Post_model):
    user_data = post_model.model_dump()
    post_id = len(post)+1
    post[post_id]=user_data
    return user_data


@app.get("/")
async def all():
    return post


