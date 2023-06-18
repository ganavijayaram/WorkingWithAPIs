from datetime import datetime, timedelta
from jose import jwt, JWTError
from . import schemas
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def createToken(data: dict):
    #To create a copy of the data, do you can preserve the actual data
    toEncode = data.copy()
    #Setting the expiration date
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    #Addind the expiration date to the data
    toEncode.update({'exp': expire})
    #Encoding the token 
    encodedJWT = jwt.encode(toEncode, SECRET_KEY, algorithm = ALGORITHM)
    return encodedJWT

#Verifying the token sent by the user in the requests
def verifyToken(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        id = payload.get("userId")
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Could not validate the Credentials", 
                                          headers = {"WWW-Authenticate": "Bearer"})
    return verifyToken(token, credentials_exception)