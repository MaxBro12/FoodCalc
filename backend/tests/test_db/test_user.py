import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import DB
from app.core.auth import verify_hashed


async def test_base_user(test_db: AsyncSession):
    users = await DB.users.all(session=test_db)
    assert len(users) == 1
    assert users[0].id == 1
    assert users[0].name == 'test12345'
    assert verify_hashed('123456', users[0].password)
