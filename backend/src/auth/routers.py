from datetime import timedelta
from fastapi import APIRouter, BackgroundTasks, Depends, Response, status

from sqlalchemy.orm import Session

from src.config import LOGGER, bucket
from src.exceptions import DetailedBadRequest
from src.database import get_db

from src.auth import crud, exceptions
from src.auth.schemas import (
    User, UserLogin, UserResponse,
    UserBase, UserRegister, AccessTokenResponse)
from src.auth.serializers import userResponseEntity
from src.auth.oa2auth import AuthJWT
from src.auth.services import authenticate_user
from src.auth.dependencies import required_user

from .config import auth_config


router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = auth_config.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = auth_config.REFRESH_TOKEN_EXPIRES_IN


@router.post("/register", status_code=status.HTTP_201_CREATED,
             response_model=UserResponse)
async def register_user(
    auth_data: UserRegister,
    db: Session = Depends(get_db)
) -> dict[str, str | dict]:
    LOGGER.info(type(auth_data))
    if await crud.get_user_by_email(db, auth_data.email):
        raise exceptions.EmailTaken()
    
    if await crud.get_user_by_username(db, auth_data.username):
        raise exceptions.UsernameTaken()
    
    user = await crud.create_user(db, auth_data)
    user_entity = userResponseEntity(user)
    return {
        "status": "success",
        "user": user_entity,
    }

@router.get('/me', response_model=UserResponse)
async def get_me(user: User = Depends(required_user)):
    user = userResponseEntity(user)
    
    return {"status": "success", "user": user}

@router.post("/login", response_model=AccessTokenResponse)
async def login(payload: UserLogin, response: Response,
                Authorize: AuthJWT = Depends(),
                db: Session = Depends(get_db)) -> AccessTokenResponse:
    user = await authenticate_user(db, payload)
    
    # Create access token
    access_token = Authorize.create_access_token(
        subject=str(user.id), fresh=True, 
        expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    # Create refresh token
    refresh_token = Authorize.create_refresh_token(
        subject=str(user.id), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

    # Store refresh and access tokens in cookie
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    # response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
    #                     ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    # response.set_cookie('refresh_token', refresh_token,
    #                     REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    return AccessTokenResponse(
        status="success", access_token=access_token
    )


@router.get('/refresh')
async def refresh_token(response: Response, 
                        Authorize: AuthJWT = Depends(),
                        db: Session = Depends(get_db)):
    try:
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise exceptions.RefreshTokenNotValid()
        user = await crud.get_user_by_id(db, int(user_id))
        if not user:
            raise exceptions.UserNotExistsWithRefreshToken()
        access_token = Authorize.create_access_token(
            subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise exceptions.RefreshTokenRequired()
        raise DetailedBadRequest(detail=error)

    # Set the JWT cookies in the response
    Authorize.set_access_cookies(access_token)
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
    return {'status': True, 'access_token': access_token}


@router.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, Authorize: AuthJWT = Depends(), 
           user: User = Depends(required_user)):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)

    return {'status': 'success'}
