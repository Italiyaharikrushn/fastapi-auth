import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = os.getenv('APP_NAME','e_commerce')
    SQLALCHEMY_DATABASE_URL: str = os.getenv("SQLALCHEMY_DATABASE_URL","postgresql://postgres:root@localhost/demo")
    SECRET_KEY: str = os.getenv('SECRET_KEY','1f4cd5d9-504f-443e-9f85-181a1ed230d0')
    REFRESH_SECRET_KEY: str = os.getenv('REFRESH_SECRET_KEY','1f4cd5d9-504f-443e-9f85-181a1ed230d0')
    ALGORITHM: str = os.getenv('ALGORITHM','HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    IS_PRODUCTION: bool = Field(default=False)

    class Config:
        case_sensitive = True
        env_file = '.env'


settings = Settings()
