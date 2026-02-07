import pytest
from httpx import AsyncClient

from app.database.repo import DataBase


async def test_correct(test_client: AsyncClient, test_db: DataBase):
    ans = await test_client.post(
        '/v1/products/new',
        json={
            'id': '1234567890123',
            'name': 'Новый тестовый продукт',
            'description': 'Описание тестового продукта',
            'minerals': [
                {
                    'id': 1,
                    'content': 100,
                }
            ],
            'calories': 100,
            'energy': 0,
        }
    )

    assert ans.status_code == 200
    assert ans.json()['ok'] == True

    await test_db.commit()

    data = await test_db.products.by_name('Новый тестовый продукт', True)
    assert data is not None
    assert data.id == '1234567890123'
    assert data.name == 'Новый тестовый продукт'
    assert data.description == 'Описание тестового продукта'
    assert data.minerals[0].mineral_id == 1
    assert data.minerals[0].content == 100
    assert data.calories == 100
    assert data.energy == 0


async def test_existing(test_client: AsyncClient, test_db: DataBase):
    ans = await test_client.post(
        '/v1/products/new',
        json={
            'id': '1000000000001',
            'name': 'Новый тестовый продукт',
            'description': 'Описание тестового продукта',
            'minerals': [
                {
                    'id': 1,
                    'content': 100,
                }
            ],
            'calories': 100,
            'energy': 0,
        }
    )

    assert ans.status_code == 409
    assert ans.json()['detail'] == 'Продукт уже существует'
