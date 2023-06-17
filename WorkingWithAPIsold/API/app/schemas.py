#For creating schema for the Post request
from pydantic import BaseModel, EmailStr
from datetime import datetime

#Creating schema for the Post request
class PostBase(BaseModel):
    #title and content has to be present and has to be string datatype
    title: str
    content: str
    #setting default value, in case the value is not provided
    published: bool = True 

class CreatePost(PostBase):
    pass

#This is the response which is sent to the user
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str