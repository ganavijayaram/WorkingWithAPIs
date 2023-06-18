from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..oauth2 import get_current_user


router = APIRouter(
    prefix = "/posts", tags = ['Posts']
)

@router.get("/", response_model = List[schemas.Post])
def getPosts(db: Session = Depends(get_db),
                 currentUser: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM POSTS""")
    #allPosts = cursor.fetchall()
    allPosts = db.query(models.Post).all()
    return allPosts


#Here when the client will send data, the data is taken by the API
#and API will send it to pur web app. so we are extracting that paylaod and returning 
#the same data to the user(we can return anything, but we are returning the data which user used)
 
@router.post("/", status_code=status.HTTP_201_CREATED,
           response_model = schemas.Post)
def createPosts(post: schemas.CreatePost, db: Session = Depends(get_db),
                 currentUser: int = Depends(oauth2.get_current_user)):
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


       
#Giving path parameter
@router.get("/{id}", response_model = schemas.Post)
#Validation provided by the FastAPI
def getPost(id: int, db: Session = Depends(get_db), 
                 currentUser: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # singlePost = cursor.fetchone()
    print(currentUser.email)
    singlePost = db.query(models.Post).filter(models.Post.id == id).first()
    if not singlePost:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
         detail = f"The post requested with id {id} does not exist")
    return singlePost

    



@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def deletePost(id: int, db: Session = Depends(get_db),
                 currentUser: int = Depends(oauth2.get_current_user)):
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
    

@router.put("/{id}", status_code = status.HTTP_200_OK, response_model = schemas.Post)
def updatePost(id: int, post: schemas.CreatePost, db: Session = Depends(get_db),
                 currentUser: int = Depends(oauth2.get_current_user)):
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
    
