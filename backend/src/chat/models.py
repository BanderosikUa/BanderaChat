import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, LargeBinary
from sqlalchemy.orm import relationship

from src.database import Base

class Message(Base):
    __tablename__ = 'message'
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    message = Column(String(1000), nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now, 
                        default=datetime.datetime.now, nullable=False)
    
    chat = relationship("Chat", back_populates="messages")  # many to one
    user = relationship("User", back_populates="messages")  # foreign key
    
class Chat(Base):
    __tablename__ = 'chat'
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String(100), nullable=False)
    is_direct = Column(Boolean, default=True, nullable=False)
    messages = relationship("Message", back_populates="chat")
    
    photo = Column(String(55), default="", nullable=False)
    
    creator = relationship("User", back_populates="chat_creator")
    moderators = relationship("User", back_populates="chat_moderator")
    participants = relationship("User", back_populates="chat_participant")
    
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now, 
                        default=datetime.datetime.now, nullable=False)
    
