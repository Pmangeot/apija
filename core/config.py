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
    HOST: str ="db"        
    DATABASE: str ="jardin_anciens"
    USER: str ="user"
    PASSWORD: str ="password"

    
    # SMTP Server
    SMTP_SERVER: str ="smtp.example.com"
    SMTP_PORT: int =587
    SMTP_USERNAME: str ="your_email@example.com"
    SMTP_PASSWORD: str ="your_password"   
    
    class Config:
        case_sensitive = True


# Instanciation
settings = Settings()
