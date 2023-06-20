from datetime import datetime, timedelta
from jose import jwt, JWTError
from . import schemas, models, database
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")



def createToken(data: dict):
    #To create a copy of the data, do you can preserve the actual data
    toEncode = data.copy()
    #Setting the expiration date
    expire = datetime.utcnow() + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    #Addind the expiration date to the data
    toEncode.update({'exp': expire})
    #Encoding the token 
    encodedJWT = jwt.encode(toEncode, settings.SECRET_KEY, algorithm = settings.ALGORITHM)
    return encodedJWT

#Verifying the token sent by the user in the requests
def verifyToken(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms = [settings.ALGORITHM])
        id = payload.get("userId")
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Could not validate the Credentials", 
                                          headers = {"WWW-Authenticate": "Bearer"})
    token  = verifyToken(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user