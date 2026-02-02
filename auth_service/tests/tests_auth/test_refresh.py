import pytest
from httpx import AsyncClient
from app.database.repo import DataBase

from core.simplejwt import SimpleJWT
from app.settings import settings


jwt = SimpleJWT(settings.AUTH_SECRET_KEY, settings.AUTH_ALGORITHM)


async def test_correct_refresh(test_client: AsyncClient, test_db: DataBase):
    tokens = await test_client.post('/v1/auth/login', json={'name': 'test_user', 'password': 'test_password'})
    ans = await test_client.post('/v1/auth/refresh', json={'refresh_token': tokens.json()['refresh_token']})
    assert ans.status_code == 200
    access_token = ans.json()['access_token']
    refresh_token = ans.json()['refresh_token']

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


async def test_incorrect_token(test_client: AsyncClient, test_db: DataBase):
    tokens = await test_client.post('/v1/auth/login', json={'name': 'test_user', 'password': 'test_password'})
    ans = await test_client.post('/v1/auth/refresh', json={'refresh_token': '123%123'})
    assert ans.status_code == 401


async def test_wrong_token_username(test_client: AsyncClient, test_db: DataBase):
    tokens = await test_client.post('/v1/auth/login', json={'name': 'test_user', 'password': 'test_password'})
    user = jwt.verify_token(tokens.json()['refresh_token'])
    wrong_token = jwt.create_token(
        payload={
            'uid': 'wrong_user',
            'usp': user.payload['usp'],
            'uni': user.payload['uni']
        }, expire_delta=settings.AUTH_REFRESH_EXPIRE_DAYS * 24 * 60 * 60)
    ans = await test_client.post('/v1/auth/refresh', json={'refresh_token': wrong_token})
    assert ans.status_code == 404


async def test_wrong_token_id(test_client: AsyncClient, test_db: DataBase):
    tokens = await test_client.post('/v1/auth/login', json={'name': 'test_user', 'password': 'test_password'})
    user = jwt.verify_token(tokens.json()['refresh_token'])
    wrong_token = jwt.create_token(
        payload={
            'uid': user.payload['uid'],
            'usp': 1123,
            'uni': user.payload['uni']
        }, expire_delta=settings.AUTH_REFRESH_EXPIRE_DAYS * 24 * 60 * 60)
    ans = await test_client.post('/v1/auth/refresh', json={'refresh_token': wrong_token})
    assert ans.status_code == 404


async def test_wrong_token_uni(test_client: AsyncClient):
    tokens = await test_client.post('/v1/auth/login', json={'name': 'test_user', 'password': 'test_password'})
    user = jwt.verify_token(tokens.json()['refresh_token'])
    wrong_token = jwt.create_token(
        payload={
            'uid': user.payload['uid'],
            'usp': user.payload['usp'],
            'uni': 'wrong_uni'
        }, expire_delta=settings.AUTH_REFRESH_EXPIRE_DAYS * 24 * 60 * 60)
    ans = await test_client.post('/v1/auth/refresh', json={'refresh_token': wrong_token})
    assert ans.status_code == 404
