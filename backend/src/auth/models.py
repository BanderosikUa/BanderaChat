import datetime
import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime

from src.database import Base, BinaryUUID

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
