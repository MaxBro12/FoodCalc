import pytest


async def test_login(test_client):
    ans = await test_client.post('/v1/auth/login', json={
        'username': 'test12345', 'password': '123456'
    })
    assert ans.status_code == 200
    assert ans.json().get('access_token') is not None
    assert ans.json().get('token_type') == 'Bearer'


async def test_login_wrong(test_client):
    ans = await test_client.post('/v1/auth/login', json={
        'username': 'test123', 'password': '123456123'
    })
    assert ans.status_code == 406
    assert ans.json().get('access_token') is None
    assert ans.json().get('token_type') is None


async def test_register_good(test_client):
    ans = await test_client.post('/v1/auth/register', json={
        'username': 'test123456',
        'password': '123456',
        'key': '12345'
    })
    assert ans.status_code == 200
    assert True == ans.json().get('ok', False)


async def test_register_short_credentials(test_client):
        ans = await test_client.post('/v1/auth/register', json={
            'username': 'test',
            'password': '123',
            'key': '12345'
        })

        assert ans.status_code == 400
        assert "Логин или пароль должны быть больше 6" in ans.json()["detail"]


async def test_register_existing_username(test_client):
    ans = await test_client.post('/v1/auth/register', json={
        'username': 'test12345',
        'password': '123456',
        'key': '12345'
    })

    assert ans.status_code == 400
    assert "Имя пользователя уже существует" in ans.json()["detail"]


async def test_register_wrong_key(test_client):
    ans = await test_client.post('/v1/auth/register', json={
        'username': 'test12345678',
        'password': '123456',
        'key': '12345896'
    })

    assert ans.status_code == 400
    assert "Ввели неправильный ключ" in ans.json()["detail"]
