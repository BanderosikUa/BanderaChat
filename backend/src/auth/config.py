import os
from pydantic import BaseSettings

from dotenv import load_dotenv

load_dotenv()

class AuthConfig(BaseSettings):
    JWT_ALGORITHM: str | None = "RS256"
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int = 60
    ACCESS_TOKEN_EXPIRES_IN: int = 60*2
    JWT_ALGORITHM: str = "RS256"
    
    CLIENT_ORIGIN: str = "http://localhost:3000"

    ALGORITHM: str = "HS256"
    # SECURE_COOKIES: bool = True
    
    class Config:
        env_file = './.env'


auth_config = AuthConfig()
