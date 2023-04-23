from src.config import LOGGER

from src.chat import schemas as chat_schemas
from src.auth import schemas as auth_schemas

from src.chat.models import Chat


def setup_default_chat_photo(user: auth_schemas.User, 
                             chats: list[Chat]) -> list[chat_schemas.Chat]:
    chats = [chat_schemas.Chat.from_orm(chat_db) for chat_db in chats]
    for chat in chats:
        if chat.is_direct and not chat.photo:
            LOGGER.info(chat.participants)
            interlocutor = None
            for participant in chat.participants:
                if user.id != participant.id:
                    interlocutor = participant
            LOGGER.info(interlocutor)
            chat.photo = interlocutor.photo if interlocutor else chat.photo
    return chats
            
