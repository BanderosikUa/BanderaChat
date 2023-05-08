from src.config import LOGGER

from src.chat import schemas as chat_schemas
from src.auth import schemas as auth_schemas

from src.chat.models import Chat


def setup_default_chat_photo_and_title(user: auth_schemas.User, 
                                      chats: list[Chat]) -> list[chat_schemas.Chat]:
    chats = [chat_schemas.Chat.from_orm(chat_db) for chat_db in chats]
    for chat in chats:
        if chat.is_direct and not chat.photo:
            interlocutor = None
            for participant in chat.participants:
                if user.id != participant.id:
                    interlocutor = participant
            chat.photo = interlocutor.photo if interlocutor else chat.photo
            chat.title = interlocutor.username if interlocutor else chat.name
    return chats
