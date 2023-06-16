#For creating schema for the Post request
from pydantic import BaseModel

#Creating schema for the Post request
class PostBase(BaseModel):
    #title and content has to be present and has to be string datatype
    title: str
    content: str
    #setting default value, in case the value is not provided
    published: bool = True 

class CreatePost(PostBase):
    pass