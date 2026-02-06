import pytest
from httpx import AsyncClient

from app.database.repo import DataBase


async def test_mineral_correct(test_db: DataBase, test_client: AsyncClient):
    await test_db.minerals.new(
        name="New Test Mineral",
        compact_name="NTM",
        description="A new mineral",
        intake=100,
        type_id=1
    )
    mineral = await test_db.minerals.by_name("New Test Mineral")
    assert mineral is not None

    ans = await test_client.delete(f"/v1/universe/minerals/{mineral.id}")
    assert ans.status_code == 200
    assert ans.json().get('ok') == True


async def test_mineral_not_found(test_db: DataBase, test_client: AsyncClient):
    ans = await test_client.delete(f"/v1/universe/minerals/9999")
    assert ans.status_code == 200
    assert ans.json().get('ok') == False


async def test_types_correct(test_db: DataBase, test_client: AsyncClient):
    await test_db.mineral_types.new(
        name="New Test Mineral Type",
        description="A new mineral",
    )
    m_type = await test_db.mineral_types.by_name("New Test Mineral Type")
    assert m_type is not None

    ans = await test_client.delete(f"/v1/universe/types/{m_type.id}")
    assert ans.status_code == 200
    assert ans.json().get('ok') == True


async def test_types_not_found(test_db: DataBase, test_client: AsyncClient):
    ans = await test_client.delete(f"/v1/universe/types/9999")
    assert ans.status_code == 200
    assert ans.json().get('ok') == False
