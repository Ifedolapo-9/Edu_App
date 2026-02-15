import os
print("DATABASE_URL =", os.getenv("DATABASE_URL"))

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "EDU_APP"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str 

    #Security 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    ALGORITHM: str = ""
    SECRET_KEY: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()