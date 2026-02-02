import pytest
from httpx import AsyncClient
from app.database.repo import DataBase
from core.security import SecurityService


async def test_correct_register(test_client: AsyncClient, test_db: DataBase):
    ans = await test_client.post("/v1/auth/register", json={
        "name": "test_new_user",
        "password": "testpassword",
        "key": "123"
    })
    assert ans.status_code == 200
    assert ans.json()["ok"] == True

    user = await test_db.users.by_name('test_new_user')
    assert user is not None
    assert user.name == 'test_new_user'
    assert SecurityService.verify('testpassword', user.password)

    await test_db.users.delete_by_name('test_new_user', True)


async def test_wrong_name_len(test_client: AsyncClient, test_db: DataBase):
    ans = await test_client.post("/v1/auth/register", json={
        "name": "user",
        "password": "testpassword",
        "key": "123"
    })
    assert ans.status_code == 400
    assert ans.json()["detail"] == "Логин или пароль должны быть больше 6"


async def test_wrong_pass_len(test_client: AsyncClient, test_db: DataBase):
    ans = await test_client.post("/v1/auth/register", json={
        "name": "username_long",
        "password": "pass",
        "key": "123"
    })
    assert ans.status_code == 400
    assert ans.json()["detail"] == "Логин или пароль должны быть больше 6"


async def test_user_exists(test_client: AsyncClient, test_db: DataBase):
    ans = await test_client.post("/v1/auth/register", json={
        "name": "test_user",
        "password": "testpassword",
        "key": "123"
    })
    assert ans.status_code == 400
    assert ans.json()["detail"] == "Имя пользователя уже существует"


async def test_wrong_key(test_client: AsyncClient, test_db: DataBase):
    ans = await test_client.post("/v1/auth/register", json={
        "name": "username_long",
        "password": "test_password",
        "key": "136"
    })
    assert ans.status_code == 400
    assert ans.json()["detail"] == "Ввели неправильный ключ"
