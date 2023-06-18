from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def createToken(data: dict):
    #To create a copy of the data, do you can preserve the actual data
    toEncode = data.copy()
    #Setting the expiration date
    expire = datetime.now() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    #Addind the expiration date to the data
    toEncode.update({'exp': expire})
    #Encoding the token 
    encodedJWT = jwt.encode(toEncode, SECRET_KEY, algorithm = ALGORITHM)
    return encodedJWT