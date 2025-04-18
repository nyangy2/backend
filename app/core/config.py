

from pydantic_settings import BaseSettings
from pydantic import EmailStr

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str
    MFDS_API_KEY: str

    class Config:
        env_file = ".env"
        extra = "forbid"

settings = Settings()
