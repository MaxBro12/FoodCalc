import pytest
from httpx import AsyncClient

from app.database.repo import DataBase


async def test_correct(test_client: AsyncClient, test_db: DataBase):
    product = await test_db.products.by_id('1000000000000')
    assert product is not None
    ans = await test_client.delete(f'/v1/products/{product.id}')
    assert ans.status_code == 200
    assert ans.json()['ok'] == True


async def test_not_exists(test_client: AsyncClient):
    ans = await test_client.delete('/v1/products/1000000000000')
    assert ans.status_code == 200
    assert ans.json()['ok'] == False
