from fastapi import HTTPException, status
from src.database import DataBase


class MineralTypesHandler:
    """
    Обработчик запросов к таблице типов минералов.
    Связывает fastapi запросы с sqlalchemy.
    """

    def __init__(self, db: DataBase):
        self.db = db

    async def all(self, skip: int | None = 0, limit: int | None = 100) -> dict:
        types = await self.db.mineral_types.all(skip=skip or 0, limit=limit or 100)
        return {'types': [{
            'id': t.id,
            'name': t.name,
            'description': t.description,
            'minerals': [{
                'id': mineral.id,
                'name': mineral.name,
                'compact_name': mineral.compact_name,
                'description': mineral.description,
            } for mineral in t.minerals]
        } for t in types]}

    async def by_id(self, mineral_id: int):
        mineral_type = await self.db.mineral_types.by_id(mineral_id)
        if not mineral_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Данный тип минерал не найден'
            )
        return mineral_type
