from datetime import datetime, timedelta, timezone

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from core.sql_repository import Repository
from app.database.models.ban import Ban

from app.settings import settings


class BanRepo(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(Ban, session=session)

    async def exists(self, ip_address: str) -> bool:
        return await self._exists(_filter=f"{self.table_name}.ip='{ip_address}'")

    async def by_ip(self, ip_address: str) -> Ban | None:
        return await self.get(_filter=f"{self.table_name}.ip='{ip_address}'")

    async def new(self, ip_address: str, reason: str | None = None, commit: bool = False) -> bool:
        try:
            if len(ip_address.split('.')) != 4:
                return False
            return await self.add(Ban(
                ip=ip_address,
                reason=reason if reason else "no reason"
            ), commit=commit)
        except IntegrityError:
            return False

    async def delete_by_ip(self, ip_address: str, commit: bool = False) -> bool:
        data = await self.by_ip(ip_address)
        if data:
            return await self.delete(obj=data, commit=commit)
        return False

    async def pagination(self, skip: int | None = None, limit: int | None = None) -> tuple[Ban, ...]:
        return await super()._pagination(
            skip=skip,
            limit=limit,
            order_by_field=f"ip",
        )

    async def del_old_bans(self):
        await self.session.execute(
            delete(Ban).where(
                Ban.date < datetime.now(timezone.utc) - timedelta(days=settings.DAYS_IN_BAN)
            )
        )
        await self.session.commit()
