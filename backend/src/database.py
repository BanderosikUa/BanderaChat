import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    LargeBinary,
    MetaData,
    String,
    Table,
    create_engine,
    func,
)
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.types import TypeDecorator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import settings, LOGGER
from src.constants import DB_NAMING_CONVENTION

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)
# metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

# database = Database(DATABASE_URL, force_rollback=settings.ENVIRONMENT.is_testing)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# class DbContext:
#     def __init__(self):
#         self.db = SessionLocal()

#     def __enter__(self):
#         return self.db

#     def __exit__(self, et, ev, traceback):
#         self.db.close()


class BinaryUUID(TypeDecorator):
    '''Optimize UUID keys. Store as 16 bit binary, retrieve as uuid.
        Working only for mysql db. 
        Use "from sqlalchemy.dialects.postgresql import UUID" for postgres
    '''
    
    impl = BINARY(16)
    
    def process_bind_param(self, value, dialect):
        try:
            return value.bytes
        except AttributeError:
            try:
                return uuid.UUID(value).bytes
            except TypeError:
                return value
                
    def process_result_value(self, value, dialect):
        return uuid.UUID(bytes=value)


# auth_user = Table(
#     "auth_user",
#     metadata,
#     Column("id", Integer, Identity(), primary_key=True),
#     Column("email", String(255), nullable=False),
#     Column("password", LargeBinary, nullable=False),
#     Column("is_admin", Boolean, default=False, nullable=False),
#     Column("created_at", DateTime, server_default=func.now(), nullable=False),
#     Column("updated_at", DateTime, onupdate=func.now()),
# )

# refresh_tokens = Table(
#     "auth_refresh_token",
#     metadata,
#     Column("uuid", BinaryUUID, primary_key=True, default=uuid.uuid4),
#     Column("user_id", ForeignKey("auth_user.id", ondelete="CASCADE"), nullable=False),
#     Column("refresh_token", String(255), nullable=False),
#     Column("expires_at", DateTime, nullable=False),
#     Column("created_at", DateTime, server_default=func.now(), nullable=False),
#     Column("updated_at", DateTime, onupdate=func.now()),
# )
