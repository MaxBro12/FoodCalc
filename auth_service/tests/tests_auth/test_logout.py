import pytest
from httpx import AsyncClient
from app.database.repo import DataBase


async def test_correct_logout(test_client: AsyncClient, test_db: DataBase):
    await test_client.post('/v1/auth/login', json={'name': 'test_user', 'password': 'test_password'})
    ans = await test_client.post('/v1/auth/logout', json={'name': 'test_user'})
    assert ans.status_code == 200
    assert ans.json()['ok'] == True

    user =await test_db.users.by_name('test_user')
    assert user.unique == ''


async def test_incorrect_logout(test_client: AsyncClient, test_db: DataBase):
    await test_client.post('/v1/auth/login', json={'name': 'test_user', 'password': 'test_password'})
    ans = await test_client.post('/v1/auth/logout', json={'name': 'test_user123'})
    assert ans.status_code == 404
    assert ans.json()['detail'] == 'User not found'

    user =await test_db.users.by_name('test_user')
    assert user.unique != ''
