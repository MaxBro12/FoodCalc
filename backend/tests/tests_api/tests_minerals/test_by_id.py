import pytest
from httpx import AsyncClient

from app.database.repo import DataBase


async def test_mineral_correct(test_client: AsyncClient, test_db: DataBase):
    mineral = await test_db.minerals.by_id(1)
    assert mineral is not None
    ans = await test_client.get(f"/v1/universe/minerals/{mineral.id}")
    assert ans.status_code == 200
    assert ans.json()["id"] == mineral.id
    assert ans.json()["name"] == mineral.name
    assert ans.json()["compact_name"] == mineral.compact_name
    assert ans.json()["description"] == mineral.description
    assert ans.json()["intake"] == mineral.intake
    assert ans.json()["type_id"] == mineral.type_id
    assert ans.json()["type_name"] == mineral.type.name


async def test_mineral_not_found(test_client: AsyncClient, test_db: DataBase):
    ans = await test_client.get("/v1/universe/minerals/999")
    assert ans.status_code == 404
    assert ans.json()["detail"] == "Минерал не найден"


async def test_type_correct(test_client: AsyncClient, test_db: DataBase):
    m_type = await test_db.mineral_types.by_id(1, True)
    assert m_type is not None
    ans = await test_client.get(f"/v1/universe/types/{m_type.id}")
    assert ans.status_code == 200
    assert ans.json()["id"] == m_type.id
    assert ans.json()["name"] == m_type.name
    assert ans.json()["description"] == m_type.description
    assert len(ans.json()['minerals']) > 0
    assert ans.json()['minerals'][0]['id'] == m_type.minerals[0].id
    assert ans.json()['minerals'][0]['name'] == m_type.minerals[0].name
    assert ans.json()['minerals'][0]['compact_name'] == m_type.minerals[0].compact_name
    assert ans.json()['minerals'][0]['description'] == m_type.minerals[0].description


async def test_type_not_found(test_client: AsyncClient, test_db: DataBase):
    ans = await test_client.get("/v1/universe/types/999")
    assert ans.status_code == 404
    assert ans.json()["detail"] == "Тип минералов не найден"
