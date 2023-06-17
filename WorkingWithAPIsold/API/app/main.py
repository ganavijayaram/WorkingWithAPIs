#fastapi is the module and FASTAPI is the class
from fastapi import FastAPI 
from fastapi.params import Body
#For creating schema for the Post request
from pydantic import BaseModel
#For creating optional parameters for Post data
from typing import Optional
from random import randrange
from fastapi import Response, status, HTTPException, Depends
#Importing all the libraries related to psycopg2
import psycopg2
#To get the values from database in the form of dictionary
from psycopg2.extras import RealDictCursor
#importing time to give a break before connecting to DB again
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

#Creating instance of the class FastAPI
app = FastAPI()



while True:
    try:
        #Connecting to the PostgreSQL
        conn = psycopg2.connect(host = "localhost", database = "WorkingWithFastAPI",
        user = "postgres", password = "", cursor_factory=RealDictCursor)
        #Creating Cursor
        cursor = conn.cursor()
        print("Database Connection Successful!")
        break
    except Exception as err:
        print("Database connection was not successful!")
        time.sleep(2)
#Using in built memory for time being
myPosts = [{"title": "Title 1", "content": " Content 1", "id": 1}, {"title": "Title 2", "content": "Content 2", "id": 2}]

#routing/path operations

#This is a decorator, inside get(), we give the path so that root() os executed
@app.get("/")
#this is the function which gets executed when / is called on the web browser
def root():
    return {"message": "Ganavi got an internship!!"}

@app.get("/posts")
def getPosts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM POSTS""")
    #allPosts = cursor.fetchall()
    allPosts = db.query(models.Post).all()
    return allPosts


#Here when the client will send data, the data is taken by the API
#and API will send it to pur web app. so we are extracting that paylaod and returning 
#the same data to the user(we can return anything, but we are returning the data which user used)
 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPosts(post: schemas.CreatePost, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, 
    #                 published) VALUES (%s, %s, %s) RETURNING *""", 
    #                (post.title, post.content, post.published))
    # newPost = cursor.fetchone()
    # conn.commit()
    #newPost = models.Posts(title = post.title, content = post.content,
                           #published = post.published)
    newPost = models.Post(**post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost
    #return {"newpost": f"title: {payload['title']} content: {payload['content']}"}

def findPost(id):
    for p in myPosts:
        if p["id"] == int(id):
            return p
       
#Giving path parameter
@app.get("/posts/{id}")
#Validation provided by the FastAPI
def getPost(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # singlePost = cursor.fetchone()
    singlePost = db.query(models.Post).filter(models.Post.id == id).first()
    if not singlePost:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
         detail = f"The post requested with id {id} does not exist")
    return singlePost

    

def findPostIndex(id):
    for i, p in enumerate(myPosts):
        if(p["id"] == id):
            return i

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def deletePost(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""",
    #                (str(id)))
    # deletedPost = cursor.fetchone()
    toDeletePost = db.query(models.Post).filter(models.Post.id == id)
    if toDeletePost.first() is not None:
        #conn.commit()
        toDeletePost.delete(synchronize_session = False)
        db.commit()
        return Response(status_code = status.HTTP_204_NO_CONTENT)
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found!")
    

@app.put("/posts/{id}", status_code = status.HTTP_200_OK)
def updatePost(id: int, post: schemas.CreatePost, db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title  = %s,
    #   content  = %s, published = %s WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, str(id)))
    # updatedPost = cursor.fetchone()
    # conn.commit()
    updatePost = db.query(models.Post).filter(models.Post.id == id)
    if updatePost.first() is not None:
        #Manually entering the values
        #updatePost.update({'title': "Updating Title", 'content': "Updating Content"}, 
                          #synchronize_session=False)
        #Getting the values from the user
        updatePost.update(post.dict(), 
                          synchronize_session=False)
        db.commit()
        return updatePost.first()
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
         detail = f"Post with id {id} Cannot be updated with new content")