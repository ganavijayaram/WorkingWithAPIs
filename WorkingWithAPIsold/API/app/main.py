#fastapi is the module and FASTAPI is the class
from fastapi import FastAPI 
from fastapi.params import Body
#For creating schema for the Post request
from pydantic import BaseModel
#For creating optional parameters for Post data
from typing import Optional, List
from random import randrange
from fastapi import Response, status, HTTPException, Depends
#Importing all the libraries related to psycopg2
import psycopg2
#To get the values from database in the form of dictionary
from psycopg2.extras import RealDictCursor
#importing time to give a break before connecting to DB again
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session

#importing the routes from routers file
from .routers import post, user, auth


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

#Including the routes which are in different files to be refresenced when called
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

#routing/path operations

#This is a decorator, inside get(), we give the path so that root() os executed
@app.get("/")
#this is the function which gets executed when / is called on the web browser
def root():
    return {"message": "Ganavi got an internship!!"}

