import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Table
from sqlalchemy.orm import relationship

from src.database import Base

chat_moderators = Table('chat_moderators', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('chat_id', Integer, ForeignKey('chat.id'))
)

chat_participants = Table('chat_participants', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('chat_id', Integer, ForeignKey('chat.id'))
)

users_read_messages = Table("users_read_messages", Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('message_id', Integer, ForeignKey('message.id'))
)

class Message(Base):
    __tablename__ = 'message'
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    message = Column(String(1000), nullable=False)
    # is_read = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now, 
                        default=datetime.datetime.now, nullable=False)
    
    # foreing keys
    chat_id = Column(Integer, ForeignKey("chat.id"))
    chat = relationship("Chat", back_populates="messages")
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="messages")
    
    # manytomany
    read_by = relationship("User", secondary=users_read_messages,
                           back_populates="read_messages")
    
class Chat(Base):
    __tablename__ = 'chat'
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String(100), nullable=False)
    is_direct = Column(Boolean, default=True, nullable=False)
    messages = relationship("Message", back_populates="chat")
    
    photo = Column(String(55), default="", nullable=False)
    
    creator_id = Column(Integer, ForeignKey("user.id"))
    creator = relationship("User", back_populates="chats_creator")
    
    # many to many
    moderators = relationship("User", secondary=chat_moderators,
                              back_populates="chats_moderator")
    participants = relationship("User", secondary=chat_participants,
                                back_populates="chats_participant")
    
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now, 
                        default=datetime.datetime.now, nullable=False)
    
