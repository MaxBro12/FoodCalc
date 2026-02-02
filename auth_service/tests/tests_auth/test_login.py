import pytest
from httpx import AsyncClient
from app.database.repo import DataBase

from core.simplejwt import SimpleJWT
from app.settings import settings


async def test_correct_login(test_client: AsyncClient):
    ans = await test_client.post('/v1/auth/login', json={'name': 'test_user', 'password': 'test_password'})
    assert ans.status_code == 200
    assert 'access_token' in ans.json()
    assert 'refresh_token' in ans.json()


async def test_valid_tokens(test_client: AsyncClient, test_db: DataBase):
    ans = await test_client.post('/v1/auth/login', json={'name': 'test_user', 'password': 'test_password'})
    assert ans.status_code == 200
    access_token = ans.json()['access_token']
    refresh_token = ans.json()['refresh_token']

    jwt = SimpleJWT(settings.AUTH_SECRET_KEY, settings.AUTH_ALGORITHM)
    user = await test_db.users.by_name('test_user')

    # Verify access token
    ans = jwt.verify_token(access_token, valid_time=settings.AUTH_ACCESS_EXPIRE)
    assert ans is not None
    assert ans.payload['uid'] == user.name
    assert ans.payload['usp'] == user.id

    # Verify refresh token
    ans = jwt.verify_token(refresh_token, valid_time=settings.AUTH_REFRESH_EXPIRE_DAYS*24*60*60)
    assert ans is not None
    assert ans.payload['uid'] == user.name
    assert ans.payload['usp'] == user.id
    assert ans.payload['uni'] == user.unique


async def test_wrong_login(test_client: AsyncClient):
    ans = await test_client.post('/v1/auth/login', json={'name': 'test_user', 'password': 'not_correct_pass'})
    assert ans.status_code == 404
    assert ans.json()['detail'] == 'Invalid user'


async def test_login_inactive_user(test_client: AsyncClient):
    ans = await test_client.post('/v1/auth/login', json={'name': 'test_deactive_user', 'password': 'test_deactive_password'})
    assert ans.status_code == 404
    assert ans.json()['detail'] == 'Invalid user'
