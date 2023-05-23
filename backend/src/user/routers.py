from fastapi import (
    APIRouter, Depends, status, UploadFile, File,
)

from sqlalchemy.orm import Session

from src.config import LOGGER
from src.database import get_db
from src.schemas import PaginationParams

from src.auth.dependencies import required_user
from src.chat.services import save_photo

from src.user import crud, exceptions
from src.user.models import User
from src.user.schemas import (
    UserResponse,
    UserResponseList,
    User as UserSchema)


router = APIRouter()


@router.get('/me')
async def get_me(user: User = Depends(required_user)) -> UserResponse:
    return {"status": True, "user": user}


@router.patch("/me")
async def update_user(payload: UserSchema,
                      user: User = Depends(required_user),
                      db: Session = Depends(get_db)) -> UserResponse:
    payload.id = user.id
    
    user = await crud.update_user(db, payload)
    
    return {"status": True, "user": user}

@router.post("/me/upload")
async def update_user(photo: UploadFile = File(...),
                      user: User = Depends(required_user),
                      db: Session = Depends(get_db)) -> UserResponse:
    extension = photo.filename.split(".")[-1]
    
    if extension not in ["jpg", "jpeg", "png"]:
        raise exceptions.PhotoExtensionNotAlllow()
    
    filename = save_photo(photo)
    user.photo = filename
    
    user = await crud.update_user(db, user)
    
    return {"status": True, "user": user}

@router.get("")
async def get_all_users(pagination: PaginationParams = Depends(),
                        user = Depends(required_user),
                        db: Session = Depends(get_db)) -> UserResponseList:
    users = await crud.get_all_users(db, pagination, user)
    
    return {"status": True, "users": users}

@router.get("/me/friends")
async def get_user_friends(pagination: PaginationParams = Depends(),
                           user = Depends(required_user),
                           db: Session = Depends(get_db)) -> UserResponseList:
    users = await crud.get_all_users(db, pagination, user)
    
    return {"status": True, "users": users}
