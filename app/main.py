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








#read all 
@app.get("/")
async def all():
    cursor.execute("""SELECT * FROM post""")
    data=cursor.fetchall()
    connect.commit()
    return data



#acess/read
@app.get("/home/{id}")
async def read_post(id:int):
    cursor.execute("""SELECT * FROM post WHERE id=%s""",(id,))
    data=cursor.fetchone()
    connect.commit()
    if not data:
        raise HTTPException(status_code=404,detail=f"not found given {id}")
    return data



#create
@app.post("/create_post")
async def create_post(post_model: Post_model):
    user_data = post_model.model_dump()
    cursor.execute("""INSERT INTO post (title,content,authore,published) 
                   VALUES(%s,%s,%s,%s) RETURNING *""",(user_data["title"],user_data["content"],user_data["authore"],user_data["published"]))
    data=cursor.fetchone()
    connect.commit()
    
    
    return data


#deletion
@app.delete("/home/{id}")
async def delete_post(id: int):

    cursor.execute(
        "DELETE FROM post WHERE id=%s RETURNING *",
        (id,)
    )

    deleted_post = cursor.fetchone()
    connect.commit()

    if not deleted_post:
        raise HTTPException(status_code=404, detail="Post does not exist")

    return {
        "message": "Post deleted successfully",
        "deleted_post": deleted_post
    }



#Update
@app.put("/home/{id}")
async def update(id: int, update_post_model: Update_Post_model):
    cursor.execute("""UPDATE post 
                   SET title=%s,content=%s
                   WHERE id=%s
                   RETURNING *""",(update_post_model.title,update_post_model.content,id))
    data=cursor.fetchone()
    connect.commit()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    
    

    return {
        "status": "update successfully",
        "updated": data
    }

    

