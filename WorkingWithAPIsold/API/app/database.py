from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
from .config import settings

#Creating connection string to the database
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'
#Creating an engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#Creating a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#class which is used by the all the models to define the tables
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
