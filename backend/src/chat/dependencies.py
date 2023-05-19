from fastapi import Depends, Form, status, HTTPException
from fastapi.encoders import jsonable_encoder

from pydantic import ValidationError

from sqlalchemy.orm import Session

from src.database import get_db
from src.config import LOGGER

from src.chat.crud import get_chat_by_id
from src.chat.schemas import Chat, ChatCreate
from src.chat.exceptions import ChatPermissionRequired, ChatNotFound

from src.auth.dependencies import websocket_required_user, required_user

from src.user.schemas import User


async def websocket_valid_chat(chat_id: int, 
                               user: User = Depends(websocket_required_user),
                               db: Session = Depends(get_db)) -> Chat:
    chat = await get_chat_by_id(db, chat_id)
    if not chat:
        raise ChatNotFound
    
    chat = Chat.from_orm(chat)
    if user not in chat.participants:
        raise ChatPermissionRequired()
    
    return chat

async def valid_chat(chat_id: int, 
                     user: User = Depends(required_user),
                     db: Session = Depends(get_db)) -> Chat:
    chat = await get_chat_by_id(db, chat_id)
    if not chat:
        raise ChatNotFound
    
    chat = Chat.from_orm(chat)
    if user not in chat.participants:
        raise ChatPermissionRequired()
    
    return chat


def chat_data_checker(data: str = Form(...)):
    try:
        model = ChatCreate.parse_raw(data)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    return model
