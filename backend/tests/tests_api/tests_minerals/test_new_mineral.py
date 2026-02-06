import pytest
from httpx import AsyncClient

from app.database.repo import DataBase


async def test_new_mineral(test_client: AsyncClient, test_db: DataBase):
    ans = await test_client.post("/v1/universe/minerals/new", json={
        "name": "New Mineral",
        "compact_name": "NM",
        "description": "A new mineral",
        "intake": 100,
        "type_id": 1
    })
    assert ans.status_code == 200
    assert ans.json()['ok'] == True

    await test_db.commit()

    data = await test_db.minerals.by_name("New Mineral")
    assert data is not None
    assert data.name == "New Mineral"
    assert data.compact_name == "NM"
    assert data.description == "A new mineral"
    assert data.intake == 100
    assert data.type_id == 1


async def test_new_type(test_client: AsyncClient, test_db: DataBase):
    ans = await test_client.post("/v1/universe/types/new", json={
        "name": "New Mineral Type",
        "description": "A new mineral type",
    })
    assert ans.status_code == 200
    assert ans.json()['ok'] == True

    await test_db.commit()

    data = await test_db.mineral_types.by_name("New Mineral Type")
    assert data is not None
    assert data.name == "New Mineral Type"
    assert data.description == "A new mineral type"
