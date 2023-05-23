from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from src.schemas import PaginationParams

from src.chat import schemas
from src.user.models import User


async def update_user(db: Session, user: schemas.User) -> User:
    updated_data = user.dict(exclude_unset=True)
    
    user_db = db.query(User).filter(User.id == user.id).first()
    user_data = jsonable_encoder(user_db)
    
    for field in user_data:
        if field in updated_data:
            setattr(user_db, field, updated_data[field])
    
    db.commit()
    db.refresh(user_db)
    
    return user_db

async def get_user_by_id(db: Session, user_id: int) -> User | None:
    select_query = db.query(User).filter(User.id == user_id)

    return select_query.one_or_none()


async def get_users_list_by_ids(db: Session, user_ids: list[int]) -> list[User]:
    select_query = db.query(User).filter(User.id.in_(user_ids))

    return select_query.all()

async def get_all_users(db: Session, pagination: PaginationParams,
                        user: User) -> list[User]:
    select_query = db.query(User).filter(User.id != user.id)
    select_query = select_query.offset(pagination.skip)
    select_query= select_query.limit(pagination.limit)

    return select_query.all()

async def get_user_friends(db: Session, pagination: PaginationParams,
                           user: User) -> list[User]:
    select_query = db.query(User).filter(User.id != user.id)
    select_query = select_query.offset(pagination.skip)
    select_query= select_query.limit(pagination.limit)

    return select_query.all()
    

async def get_user_by_email(db: Session, email: str) -> User | None:
    select_query = db.query(User).filter(User.email == email)

    return select_query.one_or_none()

async def get_user_by_username(db: Session, username: str) -> User | None:
    select_query = db.query(User).filter(User.username == username)

    return select_query.one_or_none()
