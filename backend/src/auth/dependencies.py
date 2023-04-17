from datetime import datetime

from fastapi_jwt_auth import AuthJWT
from fastapi import Cookie, Depends

from sqlalchemy.orm import Session

from src.config import LOGGER

from src.database import get_db
from src.auth import crud, exceptions

from src.auth.models import RefreshToken


def _is_valid_refresh_token(db_refresh_token: RefreshToken) -> bool:
    return datetime.utcnow() <= db_refresh_token.expires_at

def required_user(Authorize: AuthJWT = Depends(),db : Session = Depends(get_db)):
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
