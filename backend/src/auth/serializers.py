from src.auth.models import User

def userEntity(user: User) -> dict:
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "photo": user.photo,
        "verified": user.verified,
        "password": user.password,
        "created_at": str(user.created_at),
        "updated_at": str(user.updated_at),
    }


def userResponseEntity(user: User) -> dict:
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "photo": user.photo,
        "created_at": str(user.created_at),
        "updated_at": str(user.updated_at),
    }


def embeddedUserResponse(user: User) -> dict:
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "photo": user.photo,
    }


def userListEntity(users: list[User]) -> list:
    return [userEntity(user) for user in users]
