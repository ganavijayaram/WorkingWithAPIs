#To hash the password
from passlib.context import CryptContext

#Telling passlib to use the bcrypt algo
pwd_context = CryptContext(schemes = "bcrypt", deprecated = "auto")

def hash(password: str):
    return pwd_context.hash(password)