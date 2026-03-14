from datetime import datetime

from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from core.spec_time import get_current_time
from src.database import Base


class Ban(Base):
    __tablename__ = 'bans'

    ip: Mapped[str] = mapped_column(primary_key=True)
    reason: Mapped[str] = mapped_column(default="no reason") # Причина блокировки
    date_unban: Mapped[datetime] = mapped_column(DateTime, default=get_current_time()) # Дата разблокировки
    permanent: Mapped[bool] = mapped_column(default=False) # Пермабан ли
    white: Mapped[bool] = mapped_column(default=False)     # В белом списке запрещено блокироватьё
