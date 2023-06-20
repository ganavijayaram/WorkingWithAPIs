from pydantic import BaseSettings
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    #Pydantic module looks at all these environment variables as case insenstivite
    DATABASE_NAME: str
    DATABASE_PORT: str
    DATABASE_HOSTNAME: str
    DATABASE_PASSWORD: str
    DATABASE_USERNAME: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str

    class Config:
        env_file = ".env"

settings = Settings()
