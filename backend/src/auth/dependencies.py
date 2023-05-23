from datetime import datetime

from fastapi import WebSocketDisconnect
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import (
    Cookie, Depends, WebSocket, WebSocketException, 
    status, Query)

from sqlalchemy.orm import Session

from src.config import LOGGER
from src.database import get_db

from src.auth import exceptions
from src.auth.models import RefreshToken

from src.user.models import User
from src.user.crud import get_user_by_id

from src.chat.manager import manager


def _is_valid_refresh_token(db_refresh_token: RefreshToken) -> bool:
    return datetime.utcnow() <= db_refresh_token.expires_at


async def required_user(Authorize: AuthJWT = Depends(),
                        db: Session = Depends(get_db)) -> User:
    """Check if user logined and return User schema or raise error"""
    
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        user = await get_user_by_id(db, user_id)

        if not user:
            raise exceptions.AuthRequired()

        # if not user["verified"]:
        #     raise NotVerified('You are not verified')
        LOGGER.info(user)
        LOGGER.info(user.__dict__)
        
        # user = User.from_orm(user)

    except Exception as e:
        error = e.__class__.__name__
        LOGGER.error(str(e))
        if error == 'MissingTokenError':
            raise exceptions.AuthRequired()
        if error == 'UserNotFound':
            raise exceptions.UserNotExistsWithRefreshToken()
        # if error == 'NotVerified':
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED, detail='Please verify your account')
        raise exceptions.InvalidToken()
    return user

async def websocket_required_user(websocket: WebSocket,
                                #   csrf_token: str = Query(...),
                                  token: str = Query(...),
                                  Authorize: AuthJWT = Depends(),
                                  db: Session = Depends(get_db)
                                  ) -> User:
    await manager.connect(websocket)
    try:
        # Authorize.jwt_required("websocket", websocket=websocket,
        #                        csrf_token=csrf_token)
        Authorize.jwt_required("websocket", token=token)
        user_id = Authorize.get_raw_jwt(token)['sub']
        user = await get_user_by_id(db, user_id)

        
        if not user:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
        
        # user = User.from_orm(user)

    except AuthJWTException as err:
        LOGGER.error(err.message)
        data = {"error": err.message}
        await manager.on_error(ws=websocket, db=db, data=data)
    
    except WebSocketDisconnect as err:
        LOGGER.info(err)
        LOGGER.info(f"{user.id} disconnected")
        await manager.disconnect(websocket)
        
    except Exception as err:
        LOGGER.info(err)
        await manager.disconnect(websocket)

    return user
