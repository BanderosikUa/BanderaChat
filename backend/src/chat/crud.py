from fastapi import Depends

from sqlalchemy.orm import Session

from src.config import LOGGER
from src.database import get_db
from src.schemas import PaginationParams

from src.auth.crud import get_user_by_id, get_users_list_by_ids
from src.auth.schemas import User

from src.chat.schemas import MessageCreate, ChatCreate
from src.chat.models import Chat, Message


async def get_chat_by_id(db: Session, chat_id: int) -> Chat | None:
    select_query = db.query(Chat).filter(Chat.id == chat_id)

    return select_query.one_or_none()

async def create_message(db: Session, message: MessageCreate) -> None:
    message = message.dict()
    db_message = Message(**message)
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # return db_message

async def create_chat(db: Session, chat: ChatCreate, user: User) -> Chat:
    if user not in chat.participants:
        chat.participants.append(user)
    
    users_ids = [user.id for user in chat.participants]
    
    user_db = await get_user_by_id(db, user.id)
    users_db = await get_users_list_by_ids(db, users_ids)
    
    chat = chat.dict()
        
    chat['participants'] = users_db
    chat['creator'] = user_db
    
    db_chat = Chat(**chat)
    
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    
    return db_chat

async def get_chats(db: Session, 
                    pagination: PaginationParams,
                    user: User) -> list[Chat]:
    # start_index = pagination.start
    # end_index = start_index + pagination.limit
    
    select_query = db.query(Chat).filter(Chat.participants.any(id=user.id))
    select_query = select_query.offset(pagination.skip)
    select_query= select_query.limit(pagination.limit)

    return select_query.all()
