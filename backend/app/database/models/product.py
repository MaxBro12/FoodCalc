from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(default='Описание не указано')
    calories: Mapped[int] = mapped_column(default=0)
    energy: Mapped[int] = mapped_column(default=0)

    added_by: Mapped[int]

    minerals: Mapped[List['ProductMineral']] = relationship(
        back_populates='product',
        lazy='selectin',
        cascade='all, delete-orphan'
    )

    search_index: Mapped[float] = mapped_column(default=0)
