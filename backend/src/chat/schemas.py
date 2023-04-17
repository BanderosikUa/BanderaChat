from datetime import datetime

from pydantic import BaseModel

class MessageBase(BaseModel):
    user_id: int
    chat_id: int
    message: str
    
class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
