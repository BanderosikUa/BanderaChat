from fastapi import (
    APIRouter, Depends, status, UploadFile, File, Request
)

from sqlalchemy.orm import Session

from src.config import LOGGER, MEDIA_DIR
from src.database import get_db
from src.schemas import PaginationParams

from src.auth.dependencies import required_user
from src.chat.services import save_photo_locally

from src.user import crud, exceptions
from src.user.models import User
from src.user.schemas import (
    UserResponse,
    UserResponseList,
    User as UserSchema)


router = APIRouter()


@router.get('/me')
async def get_me(request: Request, 
                 user: User = Depends(required_user)) -> UserResponse:
    user.photo = request.url.replace(path=MEDIA_DIR.joinpath(user.photo).as_posix())._url
    return {"status": True, "user": user}


@router.patch("/me")
async def update_user(request: Request, payload: UserSchema,
                      user: User = Depends(required_user),
                      db: Session = Depends(get_db)) -> UserResponse:
    payload.id = user.id
    
    user = await crud.update_user(db, payload)
    user.photo = request.url.replace(path=MEDIA_DIR.joinpath(user.photo).as_posix())._url

    
    return {"status": True, "user": user}

@router.post("/me/upload")
async def update_user(request: Request, photo: UploadFile = File(...),
                      user: User = Depends(required_user),
                      db: Session = Depends(get_db)) -> UserResponse:
    extension = photo.filename.split(".")[-1]
    
    if extension not in ["jpg", "jpeg", "png"]:
        raise exceptions.PhotoExtensionNotAlllow()
    
    filename = save_photo_locally(photo)
    user.photo = filename
    
    user = await crud.update_user(db, user)
    user.photo = request.url.replace(path=MEDIA_DIR.joinpath(user.photo).as_posix())._url

    return {"status": True, "user": user}

@router.get("")
async def get_all_users(request: Request, pagination: PaginationParams = Depends(),
                        user = Depends(required_user),
                        db: Session = Depends(get_db)) -> UserResponseList:
    users = await crud.get_all_users(db, pagination, user)
    users = [request.url.replace(path=MEDIA_DIR.joinpath(user.photo).as_posix())._url for user in users]
    
    return {"status": True, "users": users}

@router.get("/me/friends")
async def get_user_friends(request: Request, pagination: PaginationParams = Depends(),
                           user = Depends(required_user),
                           db: Session = Depends(get_db)) -> UserResponseList:
    users = await crud.get_all_users(db, pagination, user)
    users = [request.url.replace(path=MEDIA_DIR.joinpath(user.photo).as_posix())._url for user in users]

    return {"status": True, "users": users}
