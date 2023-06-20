from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from ..oauth2 import get_current_user
from sqlalchemy import func


router = APIRouter(
    prefix = "/posts", tags = ['Posts']
)

@router.get("/")
#Not working need to check
#@router.get("/", response_model = List[schemas.PostOut])
def getPosts(db: Session = Depends(get_db),
                 currentUser: int = Depends(oauth2.get_current_user), limit: int = 10,
                   skip: int = 0, search: Optional[str] = ""):
    #cursor.execute("""SELECT * FROM POSTS""")
    #allPosts = cursor.fetchall()

    #select posts.id, count(votes.post_id) from posts left join votes
 #on posts.id = votes.post_id 
#group by posts.id


    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #allPosts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


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
    newPost = models.Post(owner_id = currentUser.id, **post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost
    #return {"newpost": f"title: {payload['title']} content: {payload['content']}"}


       
#Giving path parameter
@router.get("/{id}")
#@router.get("/{id}", response_model = schemas.PostOut)
#Validation provided by the FastAPI
def getPost(id: int, db: Session = Depends(get_db), 
                 currentUser: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # singlePost = cursor.fetchone()
    print(currentUser.email)

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter = True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
    #singlePost = db.query(models.Post).filter(models.Post.id == id).first()
    if not posts:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
         detail = f"The post requested with id {id} does not exist")
    return posts

    



@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def deletePost(id: int, db: Session = Depends(get_db),
                 currentUser: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""",
    #                (str(id)))
    # deletedPost = cursor.fetchone()
    toDeletePostQuery = db.query(models.Post).filter(models.Post.id == id)
    if toDeletePostQuery.first() is not None:
        #conn.commit()
        post = toDeletePostQuery.first()
        if(post.owner_id != currentUser.id):
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Not authorised to delete the post!!")
        toDeletePostQuery.delete(synchronize_session = False)
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
    updatePostQuery = db.query(models.Post).filter(models.Post.id == id)
    if updatePostQuery.first() is not None:
        #Manually entering the values
        #updatePost.update({'title': "Updating Title", 'content': "Updating Content"}, 
                          #synchronize_session=False)
        #Getting the values from the user
        posts = updatePostQuery.first()
        if(posts.owner_id != currentUser.id):
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Not authorised to udpate the post!!")
        updatePostQuery.update(post.dict(), 
                          synchronize_session=False)
        db.commit()
        return updatePostQuery.first()
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
         detail = f"Post with id {id} Cannot be updated with new content")
    
