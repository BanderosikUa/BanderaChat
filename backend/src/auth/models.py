import datetime
import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, LargeBinary
from sqlalchemy.orm import relationship

from src.database import Base, BinaryUUID

from src.chat.models import chat_participants, chat_moderators, users_read_messages


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(128), unique=True, index=True, nullable=False)
    password = Column(LargeBinary, nullable=False)
    photo = Column(String(55), default="", nullable=False)
    verified = Column(Boolean, default=False, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now, 
                        default=datetime.datetime.now, nullable=False)
    
    tokens = relationship("RefreshToken")
    
    # many to one
    chats_creator = relationship("Chat", back_populates="creator")
    messages = relationship("Message", back_populates="user")
    
    # many to many
    chats_moderator = relationship("Chat", secondary=chat_moderators,
                                   back_populates="moderators")
    chats_participant = relationship("Chat", secondary=chat_participants,
                                     back_populates="participants")
    read_messages = relationship("Message", secondary=users_read_messages,
                                 back_populates="read_by")


class RefreshToken(Base):
    __tablename__ = 'refresh_token'
    
    uuid = Column(BinaryUUID, primary_key=True, default=uuid.uuid4, 
                  nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    refresh_token = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now, 
                        default=datetime.datetime.now, nullable=False)
