import pytest
import pytest_asyncio

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from fastapi import status

from src.config import LOGGER
from src.chat.constants import ErrorCode
from src.auth.crud import create_user
from src.auth.schemas import UserRegister

@pytest_asyncio.fixture
async def access_token(client: TestClient, db: Session) -> str:
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
    return access_token

@pytest.mark.asyncio
class TestChatRouters:
    async def test_chat_create(self, client: TestClient, db:Session, access_token: str):
        user_2 = UserRegister(username='test2', email='test2@world.com',
                              password="@Test123", passwordConfirm="@Test123")
        user_2_db = await create_user(db, user_2)
        resp = await client.post(
            "/chats",
            json={
                "title": "test",
                "participants": [{"id": user_2_db.id}],
            },
            headers={"Autorization": f"Bearer {access_token}"}
        )
        resp_json = resp.json()
        LOGGER.info(resp_json)
        
        assert resp.status_code == status.HTTP_200_OK
        assert resp_json['status'] == True

    async def test_error_chat_create_without_participants(self, client: TestClient, db:Session, access_token: str):
        user_2 = UserRegister(username='test2', email='test2@world.com',
                              password="@Test123", passwordConfirm="@Test123")
        user_2_db = await create_user(db, user_2)
        resp = await client.post(
            "/chats",
            json={
                "title": "test",
                "participants": [],
            },
            headers={"Autorization": f"Bearer {access_token}"}
        )
        resp_json = resp.json()
        LOGGER.info(resp_json)
        
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert resp_json['status'] == False
        assert resp_json['detail'][0]["participants"] == ErrorCode.ListOfTwoObjs
        
