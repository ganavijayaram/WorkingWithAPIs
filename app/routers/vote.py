from .. import models, schemas, utils, oauth2
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import and_

router = APIRouter(
    prefix = "/vote",
    tags = ["Vote"]
)

@router.post("/", status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db),
          current_user: int = Depends(oauth2.get_current_user)):
    #to check if the post is present
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"No Post found")
    
    #Any user is authorised to vote
   
    #Check if this user has already liked the post
    voteQuery = db.query(models.Vote).filter(and_(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id))
    found_vote =  voteQuery.first()
    
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code =  status.HTTP_409_CONFLICT, 
                            detail = f"User with id {current_user.id} already liked the post")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                                detail = f"Post with id {vote.post_id} not found")
        
        voteQuery.delete(synchronize_session = False)
        db.commit()

        return {"message": "Successfully deleted the vote"}

