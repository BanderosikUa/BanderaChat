from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.schemas import PaginationParams
from src.config import LOGGER

from src.chat.schemas import MessageCreate, ChatCreate, ChatUpdate
from src.chat.models import Chat, Message
from src.chat.exceptions import DirectChatAlreadyExists, DirectParticipantListMustHave2Objs, ChatUserNotExists

from src.user.crud import get_user_by_id, get_users_list_by_ids
from src.user.models import User
from src.user.schemas import User as UserSchema



async def get_chat_by_id(db: Session, chat_id: int) -> Chat | None:
    select_query = db.query(Chat).filter(Chat.id == chat_id)

    return select_query.one_or_none()

async def create_message(db: Session, message: MessageCreate) -> None:    
    db_message = Message(user_id=message.user.id, 
                         chat_id=message.chat.id,
                         message=message.message)
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    return db_message

async def create_chat(db: Session, chat: ChatCreate, user: UserSchema) -> Chat:
    if user not in chat.participants:
        chat.participants.append(user)
    
    users_ids = [user.id for user in chat.participants]
    
    if len(users_ids) == 1:
        raise DirectParticipantListMustHave2Objs
    
    user_db = await get_user_by_id(db, user.id)
    users_db = await get_users_list_by_ids(db, users_ids)
    
    if len(users_db) == 1:
        raise ChatUserNotExists
    
    if len(users_db) == 2:
        if await get_direct_chat_by_particips(db, users_db):
            raise DirectChatAlreadyExists
        chat.is_direct = True
        chat.title = f"{chat.participants[0].username} - {chat.participants[1].username}" 
    
    chat = chat.dict()
        
    chat['participants'] = users_db
    chat['creator'] = user_db
    
    db_chat = Chat(**chat)
    
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    
    return db_chat

async def update_chat(db: Session, chat: ChatUpdate) -> Chat:
    updated_data = chat.dict(exclude_unset=True)
    
    chat_db = db.query(Chat).filter(Chat.id == chat.id).first()
    chat_data = jsonable_encoder(chat_db)
    
    for field in chat_data:
        if field in updated_data:
            setattr(chat_db, field, updated_data[field])
    
    db.commit()
    db.refresh(chat_db)
    
    return chat_db

async def get_direct_chat_by_particips(db: Session, participants: list[User]) -> Chat:
    if len(participants) != 2:
        raise DirectParticipantListMustHave2Objs
    user1, user2 = participants
    # participants_ids = [user.id for user in participants]
    select_query = db.query(Chat).filter(
        Chat.participants.any(id=user1.id),
        Chat.participants.any(id=user2.id),
        Chat.is_direct == True
        )
    
    return select_query.one_or_none()

async def get_chats(db: Session, 
                    pagination: PaginationParams,
                    user: UserSchema) -> list[Chat]:
    # start_index = pagination.start
    # end_index = start_index + pagination.limit
    
    select_query = db.query(Chat).filter(Chat.participants.any(id=user.id))
    select_query = select_query.offset(pagination.skip)
    select_query= select_query.limit(pagination.limit)

    return select_query.all()

async def get_messages_by_chat_id(db: Session,
                                  chat_id: int) -> list[Message]:
    select_query = db.query(Message).filter(Message.chat.has(Chat.id == chat_id))

    return select_query.all()
