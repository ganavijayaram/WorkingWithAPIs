from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 

#Creating connection string to the database
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:@localhost/WorkingWithFastAPI'

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