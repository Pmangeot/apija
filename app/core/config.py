import pathlib
from pydantic_settings import BaseSettings
from typing import List

ROOT = pathlib.Path(__file__).resolve().parent.parent

class Settings(BaseSettings):

    #configuration du CORS
    ORIGINS: List[str] = [
        "*"
        # "http://localhost",
        # "http://localhost:4200",
    ]

    # URL de base de l'API
    API_STR: str = "/api"

    # JWT
    SECRET_KEY: str = "qvze46Vser§GSV"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60       # 60 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

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
