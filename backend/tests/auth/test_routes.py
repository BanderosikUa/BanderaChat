import pytest

# from fastapi import FastAPI
# from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from fastapi import status

from src.config import LOGGER
from src.auth.constants import ErrorCode
from src.auth.crud import create_user
from src.auth.schemas import UserRegister


@pytest.mark.asyncio
class TestAuthRouters:

    async def test_register(self, client: TestClient, db: Session) -> None:
        resp = await client.post(
            "/auth/register",
            json={
                "username": "bandera9",
                "email": "hello9@world.com",
                "password": "!Qwerty123",
                "passwordConfirm": "!Qwerty123",
            }
        )
        resp_json = resp.json()

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp_json['status'] == True
        
    async def test_register_email_taken(self, client: TestClient, db: Session) -> None:
        user_1 = UserRegister(username='test1', email='test1@world.com',
                              password="!Qwerty123", passwordConfirm="!Qwerty123")
        user = await create_user(db, user_1)
        resp = await client.post(
            "/auth/register",
            json={
                "username": "test1",
                "email": "test1@world.com",
                "password": "!Qwerty123",
                "passwordConfirm": "!Qwerty123",
            }
        )
        resp_json = resp.json()

        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert resp_json['detail'][0]['email'] == ErrorCode.EMAIL_TAKEN
        
    async def test_register_username_taken(self, client: TestClient, db: Session) -> None:
        user_1 = UserRegister(username='test1', email='test1@world.com',
                              password="@Test123", passwordConfirm="@Test123")
        await create_user(db, user_1)
        resp = await client.post(
            "/auth/register",
            json={
                "username": "test1",
                "email": "test2@gmail.com",
                "password": "!Qwerty123",
                "passwordConfirm": "!Qwerty123",
            }
        )
        resp_json = resp.json()

        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert resp_json['detail'][0]['username'] == ErrorCode.USERNAME_TAKEN
    
    async def test_register_passwords_not_matches(self, client: TestClient, db: Session) -> None:
        resp = await client.post(
            "/auth/register",
            json={
                "username": "test1",
                "email": "test2@gmail.com",
                "password": "!Qwerty123",
                "passwordConfirm": "!Qwerty",
            }
        )
        resp_json = resp.json()

        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert resp_json['detail'][0]['passwordConfirm'] == ErrorCode.PASSWORD_NOT_MATCH
        
    async def test_login(self, client: TestClient, db: Session):
        user_1 = UserRegister(username='test1', email='test1@world.com',
                        password="@Test123", passwordConfirm="@Test123")
        await create_user(db, user_1)
        resp = await client.post(
            "/auth/login",
            json={
                "email": "test1@world.com",
                "password": "@Test123",
            }
        )
        resp_json = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_json['status'] == True
        
    async def test_wrong_login(self, client: TestClient, db: Session):
        user_1 = UserRegister(username='test1', email='test1@world.com',
                              password="@Test123", passwordConfirm="@Test123")
        await create_user(db, user_1)
        resp = await client.post(
            "/auth/login",
            json={
                "email": "test1@world.com",
                "password": "@Test1234",
            }
        )
        resp_json = resp.json()

        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
        assert resp_json['status'] == False
        assert resp_json['detail'] == ErrorCode.INVALID_CREDENTIALS
        
    async def test_refresh_token(self, client: TestClient, db: Session):
        user_1 = UserRegister(username='test1', email='test1@world.com',
                        password="@Test123", passwordConfirm="@Test123")
        await create_user(db, user_1)
        resp = await client.post(
            "/auth/login",
            json={
                "email": "test1@world.com",
                "password": "@Test123",
            }
        )
        access_token = resp.json()['access_token']
        resp = await client.get(
            "/auth/refresh",
            headers={"Autorization": f"Bearer {access_token}"}
        )
        resp_json = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_json['status'] == True
        
