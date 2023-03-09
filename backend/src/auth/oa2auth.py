import base64
from typing import List
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

from fastapi import Depends, Cookie

from sqlalchemy.orm import Session

from src.auth.config import auth_config
from src.auth import crud, exceptions
from src.auth.dependencies import get_db

class Settings(BaseModel):
    authjwt_algorithm: str = auth_config.JWT_ALGORITHM
    authjwt_decode_algorithms: List[str] = [auth_config.JWT_ALGORITHM]
    authjwt_token_location: set = {'cookies', 'headers'}
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_public_key: str = base64.b64decode(
        auth_config.JWT_PUBLIC_KEY).decode('utf-8')
    authjwt_private_key: str = base64.b64decode(
        auth_config.JWT_PRIVATE_KEY).decode('utf-8')


@AuthJWT.load_config
def get_config():
    return Settings()

def required_user(Authorize: AuthJWT = Depends(), db : Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        user = crud.get_user_by_id(db, user_id)

        if not user:
            raise exceptions.AuthRequired()

        # if not user["verified"]:
        #     raise NotVerified('You are not verified')

    except Exception as e:
        error = e.__class__.__name__
        # LOGGER.error(error)
        if error == 'MissingTokenError':
            raise exceptions.AuthRequired()
        if error == 'UserNotFound':
            raise exceptions.UserNotExistsWithRefreshToken()
        # if error == 'NotVerified':
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED, detail='Please verify your account')
        raise exceptions.InvalidToken()
    return user_id
