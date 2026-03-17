from fastapi import FastAPI, HTTPException,status,Depends
from typing import List
from . import models,schemas
from .database import engine,get_db
from sqlalchemy.orm import Session

app = FastAPI()


#sql alchemy connection
models.Base.metadata.create_all(bind=engine)






#DB connection  
#while True:
#    try:
#    
#        connect=psycopg2.connect(host='localhost',database='CRUD',user='postgres',password='nipurn',cursor_factory=RealDictCursor)
#        cursor=connect.cursor()
#        print("sucessfully connected to DB")
#        break
#    except Exception as ex:
#        print(ex)
#       time.sleep(4)
    










#read all 
@app.get("/posts",response_model=List[schemas.Response_read])
async def all(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM post""")
    #data=cursor.fetchall()
    #connect.commit()


    data=db.query(models.Post).all()
    return data


    


#acess/read
@app.get("/home/{id}",status_code=status.HTTP_201_CREATED,response_model=schemas.Response_read)
async def read_post(id:int,db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM post WHERE id=%s""",(id,))
    #data=cursor.fetchone()
    #connect.commit()

    data=db.query(models.Post).filter(models.Post.id==id).first()
    if not data:
        raise HTTPException(status_code=404,detail=f"not found given {id}")
    return data



#create
@app.post("/create_post",response_model=schemas.Response_create)
async def create_post(post_create: schemas.Post_create,db:Session=Depends(get_db)):

    #user_data = post_model.model_dump()
    #cursor.execute("""INSERT INTO post (title,content,authore,published) 
    #               VALUES(%s,%s,%s,%s) RETURNING *""",(user_data["title"],user_data["content"],user_data["authore"],user_data["published"]))
    #data=cursor.fetchone()
    #connect.commit()



    data=models.Post(title=post_create.title,content=post_create.content,authore=post_create.authore,published=post_create.published)
    db.add(data)       
    db.commit()            
    db.refresh(data)
    return data


#deletion
@app.delete("/home/{id}")
async def delete_post(id: int,db:Session=Depends(get_db)):

    #cursor.execute(
    #    "DELETE FROM post WHERE id=%s RETURNING *",
    #    (id,)
    #)
    #deleted_post = cursor.fetchone()
    #connect.commit()

    deleted_post=db.query(models.Post).filter(models.Post.id==id)

    if not deleted_post.first():
        raise HTTPException(status_code=404, detail="Post does not exist")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    

    return {
        "message": "Post deleted successfully",
        "deleted_post": deleted_post.first()
    }



#Update
@app.put("/home/{id}",response_model=schemas.Response_update)
async def update(id: int, post_update: schemas.Post_update,db:Session=Depends(get_db)):
    #cursor.execute("""UPDATE post 
    #               SET title=%s,content=%s
    #               WHERE id=%s
    #               RETURNING *""",(update_post_model.title,update_post_model.content,id))
    #data=cursor.fetchone()
    #connect.commit()


    post_querry=db.query(models.Post).filter(models.Post.id==id)


    if not  post_querry.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    
    post_querry.update(post_update.model_dump(),synchronize_session=False)
    db.commit()
    return post_querry.first()

    

