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
    message: str
    
class MessageCreate(MessageBase):
    chat: Chat

class Message(MessageBase):
    id: int
    chat: Chat
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
        
class MessageResponse(MessageBase):
    id: int
    created_at: datetime
    updated_at: datetime
    type: Optional[str]  # own message or other
    
    class Config:
        orm_mode = True
        
class WsData(BaseModel):
    action: str = ""
    user: User
    message: MessageResponse
    
class ChatDetailResponse(BaseModel):
    status: bool
    chat: Chat
    messages: List[MessageResponse]
