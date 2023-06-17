from .. import models, schemas, utils
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/users", tags = ['Users']
)

@router.post("/", status_code = status.HTTP_201_CREATED, 
          response_model = schemas.UserOut)
def createUsers(user: schemas.UserCreate, db: Session  = Depends(get_db)):

    user.password = utils.hash(user.password)

    newUser = models.User(**user.dict())
    db.add(newUser)
    db.commit()
    #This is to return the value to the suer
    db.refresh(newUser)
    return newUser


@router.get("/{id}", status_code = status.HTTP_200_OK,
          response_model = schemas.UserOut)
def getUsers(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail = f"User with id {id} not found")
    return user