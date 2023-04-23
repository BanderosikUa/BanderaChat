from datetime import datetime

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import (
    Cookie, Depends, WebSocket, WebSocketException, 
    status, Query)

from sqlalchemy.orm import Session

from src.config import LOGGER

from src.database import get_db
from src.auth import crud, exceptions
from src.auth.schemas import User

from src.auth.models import RefreshToken

from src.chat.manager import manager

def _is_valid_refresh_token(db_refresh_token: RefreshToken) -> bool:
    return datetime.utcnow() <= db_refresh_token.expires_at

async def required_user(Authorize: AuthJWT = Depends(),
                        db: Session = Depends(get_db)) -> User:
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        user = await crud.get_user_by_id(db, user_id)

        if not user:
            raise exceptions.AuthRequired()

        # if not user["verified"]:
        #     raise NotVerified('You are not verified')

    except Exception as e:
        error = e.__class__.__name__
        LOGGER.error(error)
        if error == 'MissingTokenError':
            raise exceptions.AuthRequired()
        if error == 'UserNotFound':
            raise exceptions.UserNotExistsWithRefreshToken()
        # if error == 'NotVerified':
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED, detail='Please verify your account')
        raise exceptions.InvalidToken()
    return User.from_orm(user)

async def websocket_required_user(websocket: WebSocket,
                                  csrf_token: str = Query(...),
                                  Authorize: AuthJWT = Depends(),
                                  db: Session = Depends(get_db)
                                  ) -> User:
    LOGGER.info(csrf_token)
    await manager.connect(websocket)
    try:
        Authorize.jwt_required("websocket", websocket=websocket,
                               csrf_token=csrf_token)
        await websocket.send_text("Successfully Login!")
        user_id = Authorize.get_raw_jwt()
        user = await crud.get_user_by_id(db, user_id)

        if not user:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

        # if not user["verified"]:
        #     raise NotVerified('You are not verified')

    except AuthJWTException as err:
        await websocket.send_text(err.message)
        await websocket.close()
        raise err
    return User.from_orm(user)
