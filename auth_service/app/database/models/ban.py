from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Ban(Base):
    __tablename__ = 'bans'
    ip: Mapped[str] = mapped_column(String, primary_key=True)
    reason: Mapped[str] = mapped_column(String, default="no reason")
    date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
