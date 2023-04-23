import base64
from typing import List
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

from fastapi import Depends, Cookie

from sqlalchemy.orm import Session

from src.database import get_db

from src.auth.config import auth_config
from src.auth import crud, exceptions

class Settings(BaseModel):
    authjwt_token_location: set = {'cookies', 'headers'}
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_cookie_secure: bool = False
    # Enable csrf double submit protection. default is True
    authjwt_cookie_csrf_protect: bool = False
    # Change to 'lax' in production to make your website more secure from CSRF Attacks, default is None
    # authjwt_cookie_samesite: str = 'lax'
    authjwt_secret_key: str = "secret"
    authjwt_public_key: str = base64.b64decode(
        auth_config.JWT_PUBLIC_KEY).decode('utf-8')
    authjwt_private_key: str = base64.b64decode(
        auth_config.JWT_PRIVATE_KEY).decode('utf-8')


@AuthJWT.load_config
def get_config():
    return Settings()
