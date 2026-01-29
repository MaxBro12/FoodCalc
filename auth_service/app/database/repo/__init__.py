from sqlalchemy.ext.asyncio import AsyncSession

from core.sql_repository import DataBaseRepo
from .key import KeyRepo
from .user import UserRepo


class DataBase(DataBaseRepo):
    def __init__(self, session: AsyncSession) -> None:
        self.users = UserRepo(session=session)
        self.keys = KeyRepo(session=session)
        super().__init__(session=session)
