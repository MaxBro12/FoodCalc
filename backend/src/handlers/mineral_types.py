from fastapi import HTTPException, status
from src.database import DataBase, MineralType


class MineralTypesHandler:
    """
    Обработчик запросов к таблице типов минералов.
    Связывает fastapi запросы с sqlalchemy.
    """

    def __init__(self, db: DataBase):
        self.db = db

    @staticmethod
    def _mineral_type_to_dict(mineral_type: MineralType) -> dict:
        """
        Сериализует объект MineralType в словарь.
        """
        return {
            'id': mineral_type.id,
            'name': mineral_type.name,
            'description': mineral_type.description,
            'minerals': [{
                'id': mineral.id,
                'name': mineral.name,
                'compact_name': mineral.compact_name,
                'description': mineral.description,
            } for mineral in mineral_type.minerals]
        }

    async def all(self, skip: int | None = 0, limit: int | None = 100) -> dict:
        types = await self.db.mineral_types.all(skip=skip or 0, limit=limit or 100)
        return {'types': [self._mineral_type_to_dict(t) for t in types]}

    async def by_id(self, mineral_id: int) -> dict:
        mineral_type = await self.db.mineral_types.by_id(mineral_id, load_relations=True)
        if not mineral_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Данный тип минерал не найден'
            )
        return self._mineral_type_to_dict(mineral_type)
