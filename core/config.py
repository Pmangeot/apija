import pathlib
from pydantic_settings import BaseSettings
from typing import Optional

ROOT = pathlib.Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    API_STR: str = "/api"

    JWT_SECRET: str = "qvze46Vser§GSV"
    ALGORITHM: str = "HS256"

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # PostgreSQL Database
    SQLALCHEMY_DATABASE_URI: Optional[str] = 'postgresql://user:password@db:5432/dbname'

    class Config:
        case_sensitive = True


# Instanciation
settings = Settings()
