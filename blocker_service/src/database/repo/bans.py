from datetime import datetime, timedelta, timezone

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, and_

from core.sql_repository import Repository
from core.spec_time import time_with_shift, get_current_time
from src.database.models.ban import Ban

from src.settings import settings


class BanRepo(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(Ban, session=session)

    async def exists(self, ip_address: str, white: bool = False) -> bool:
        """
        Возвращает True если в базе есть запись адреса
        """
        return await self._exists(
            _filter=f"{self.table_name}.ip='{ip_address}' AND {self.table_name}.white={white}"
        )

    async def by_ip(self, ip_address: str) -> Ban | None:
        """
        Возвращает модель Ban если найден в базе или None
        """
        return await self.get(_filter=f"{self.table_name}.ip='{ip_address}'")

    async def new(
        self,
        ip: str,
        reason: str = 'no reason',
        duration_days: int = 3,
        permanent: bool = False,
        white: bool = False,
        commit: bool = False
    ) -> bool:
        """
        Создает в базе новую запись типа Ban.
        """
        try:
            # Проверка на то действительно ли это ipv4
            if len(ip.split('.')) != 4:
                return False
            return await self.add(Ban(
                ip=ip,
                reason=reason if reason else "no reason",
                date_unban=time_with_shift(duration_days),
                permanent=permanent,
                white=white,
            ), commit=commit)
        except IntegrityError:
            # На случай если была попытка еще раз сохранить существующий ipv4
            return False

    async def delete_by_ip(self, ip_address: str, commit: bool = False) -> bool:
        """
        Удаляем из базы запись по ip адрессу
        """
        # Ищем модель в базе данных
        data = await self.by_ip(ip_address)
        if data:
            return await self.delete(obj=data, commit=commit)
        return False

    async def pagination(self, skip: int | None = None, limit: int | None = None) -> tuple[Ban, ...]:
        """
        Пагинация записей в базе.
        """
        return await super()._pagination(
            skip=skip,
            limit=limit,
            order_by_field=f"ip",
        )

    async def del_old_bans(self):
        """
        Автоочистка старых записей
        """
        await self.session.execute(
            delete(Ban).where(
                and_(
                    Ban.date_unban < get_current_time(), # Дата разбана меньше текущей
                    Ban.permanent == False,              # Игнорируются пермабаны
                    Ban.white == False                   # Игнорируются белые списки
                )
            )
        )
        #await self.session.commit() # коммит не нужен в системе есть автокоммит
