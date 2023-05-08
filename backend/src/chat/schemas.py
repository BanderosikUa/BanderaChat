from datetime import datetime
from typing import List, Optional

from src.schemas import AllOptional

from src.auth.schemas import User

from pydantic import BaseModel

        
class ChatBase(BaseModel):
    title: Optional[str]
    participants: List[User] = []
    is_direct: bool = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
class ChatCreate(ChatBase):
    pass
    
class Chat(ChatBase, metaclass=AllOptional):
    id: int
    # messages: List[Message] = []
    is_direct: bool
    photo: str
    moderators: List[User] = []

    class Config:
        orm_mode = True
    
class ChatResponse(BaseModel):
    status: bool
    chat: Chat
    

class ChatListResponse(BaseModel):
    status: bool
    chats: List[Chat]

class MessageBase(BaseModel):
    user: User
    chat: Chat
    message: str
    
class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
        
class WsData(BaseModel):
    action: str = ""
    user: User
    message: Message
    
class ChatDetailResponse(BaseModel):
    status: bool
    chat: Chat
    messages: List[Message]
