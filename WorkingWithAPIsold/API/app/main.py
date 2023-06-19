#fastapi is the module and FASTAPI is the class
from fastapi import FastAPI 
from . import models
from .database import engine
#importing the routes from routers file
from .routers import post, user, auth, vote


#Creating instance of the class FastAPI
app = FastAPI()

#Including the routes which are in different files to be refresenced when called
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#routing/path operations

#This is a decorator, inside get(), we give the path so that root() os executed
@app.get("/")
#this is the function which gets executed when / is called on the web browser
def root():
    return {"message": "Ganavi got an internship!!"}

