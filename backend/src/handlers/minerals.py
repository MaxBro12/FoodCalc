from fastapi import HTTPException, status
from src.database import DataBase


class MineralsHandler:
    """
    Обработчик запросов к таблице минералов.
    Связывает fastapi запросы с sqlalchemy.
    Используется только если данные нужно конвертировать.
    """

    def __init__(self, db: DataBase):
        self.db = db

    async def all(self, skip: int | None = 0, limit: int | None = 100) -> dict:
        minerals = await self.db.minerals.all(skip=skip or 0, limit=limit or 100)
        return {'minerals': [{
            'id': mineral.id,
            'name': mineral.name,
            'compact_name': mineral.compact_name,
            'description': mineral.description,
            'daily_value': mineral.daily_value,
            'type_id': mineral.type_id,
            'type_name': mineral.type.name,
        } for mineral in minerals]}

    async def by_id(self, mineral_id: int) -> dict:
        mineral = await self.db.minerals.by_id(mineral_id)
        if not mineral:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Данный минерал не найден'
            )
        return {
            'id': mineral.id,
            'name': mineral.name,
            'compact_name': mineral.compact_name,
            'description': mineral.description,
            'daily_value': mineral.daily_value,
            'type_id': mineral.type_id,
            'type_name': mineral.type.name,
        }
