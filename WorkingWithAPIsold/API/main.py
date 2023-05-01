#fastapi is the module and FASTAPI is the class
from fastapi import FastAPI 
from fastapi.params import Body
#For creating schema for the Post request
from pydantic import BaseModel
#For creating optional parameters for Post data
from typing import Optional
from random import randrange
from fastapi import Response, status
#Creating instance of the class FastAPI
app = FastAPI()


#Creating schema for the Post request
class Post(BaseModel):
    #title and content has to be present and has to be string datatype
    title: str
    content: str
    #setting default value, in case the value is not provided
    rating: Optional[int] = None
    published: bool = True 

#Using in built memory for time being
myPosts = [{"title": "Title 1", "content": " Content 1", "id": 1}, {"title": "Title 2", "content": "Content 2", "id": 2}]

#routing/path operations

#This is a decorator, inside get(), we give the path so that root() os executed
@app.get("/")
#this is the function which gets executed when / is called on the web browser
def root():
    return {"message": "Ganavi got an internship!!"}


@app.get("/posts")
def getPosts():
    return {"data": myPosts}


#Here when the client will send data, the data is taken by the API
#and API will send it to pur web app. so we are extracting that paylaod and returning 
#the same data to the user(we can return anything, but we are returning the data which user used)
 
@app.post("/posts")
def createPosts(post: Post):
    print(post)
    #converting to dict
    newPost = post.dict()
    newPost["id"] = randrange(0, 1000000)
    myPosts.append(newPost)
    return {"data": newPost}
    #return {"newpost": f"title: {payload['title']} content: {payload['content']}"}

def findPost(id):
    for p in myPosts:
        if p["id"] == int(id):
            return p
       
#Giving path parameter
@app.get("/posts/{id}")
#Validation provided by the FastAPI
def getPost(id: int, response: Response):
    print(id)
    singlePost = findPost(id)
    if not singlePost:
        response.status_code = 404
    return {"Get Post with id": findPost(id)}

