from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel, Field
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

#DB connection  
while True:
    try:
    
        connect=psycopg2.connect(host='localhost',database='CRUD',user='postgres',password='nipurn',cursor_factory=RealDictCursor)
        cursor=connect.cursor()
        print("sucessfully connected to DB")
        break
    except Exception as ex:
        print(ex)
        time.sleep(4)
    

class Post_model(BaseModel):
    title: str = Field(..., max_length=40, min_length=10)
    content: str = Field(..., min_length=40, max_length=10000)
    published: bool = Field(default=True)
    authore: str  = Field(default=None,min_length=2)


class Update_Post_model(BaseModel):
    title: str = Field(..., max_length=40, min_length=10)
    content:str= Field(...,max_length=10000, min_length=40 )



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




#read all 
@app.get("/")
async def all():
    return post



#acess/read
@app.get("/home/{id}")
async def read_post(id:int):
    users_post_data = post.get(id)
    if not users_post_data:
        raise HTTPException(status_code=404,detail=f"not found given {id}")
    return users_post_data



#create
@app.post("/create_post")
async def create_post(post_model: Post_model):
    user_data = post_model.model_dump()
    post_id = len(post)+1
    post[post_id]=user_data
    return user_data



#deletion
@app.delete("/home/{id}")
async def delete_post(id: int):

    if id not in post:
        raise HTTPException(status_code=404, detail="Post does not exist")

    deleted_post = post.pop(id)

    return {
        "message": "Post deleted successfully",
        "deleted_post": deleted_post["title"]
    }



#Update
@app.put("/home/{id}")
async def update(id: int, update_post_model: Update_Post_model):
    if id not in post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    
    
    existing_post = post[id]
    updated_data = update_post_model.model_dump()
    existing_post.update(updated_data)  
    
    
    post[id] = existing_post

    return {
        "status": "update successfully",
        "updated": existing_post
    }

    

