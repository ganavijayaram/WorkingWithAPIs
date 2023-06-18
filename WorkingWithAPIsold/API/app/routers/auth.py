from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models, utils, oauth2
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags = ['Authentication'])

@router.post("/login")
def login(userCredentials: OAuth2PasswordRequestForm = Depends(),
           db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == userCredentials.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Invalid Credentials")

    if not utils.verify(userCredentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Invalid Credentials")
    
    #Create Token
   
    accessToken = oauth2.createToken(data = {'userId': user.id})
    #Send the Token
    return {"Token": accessToken, "token_type": "bearer"}
    
