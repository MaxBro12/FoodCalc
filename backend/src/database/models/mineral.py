from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.database import Base
from src.database.models import MineralType


class Mineral(Base):
    """
    Модель минерала.
    - `id`: идентификатор минерала
    - `name`: название минерала
    - `compact_name`: сокращенное название минерала
    - `description`: описание минерала
    - `daily_value`: рекомендуемое потребление минерала в милиграммах в день
    - `type_id`: идентификатор типа минерала
    - `type`: связь с моделью типа минерала
    - `products`: связь с моделью продукта
    """
    __tablename__ = 'minerals'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    compact_name: Mapped[str] = mapped_column(unique=True, nullable=False) # Сокращенное имя
    description: Mapped[str]
    daily_value: Mapped[float]

    type_id: Mapped[int] = mapped_column(ForeignKey('mineral_types.id'))
    type: Mapped[MineralType] = relationship(MineralType, back_populates='minerals', lazy='selectin')

    products: Mapped[List['ProductMineral']] = relationship(
        back_populates='mineral'
    )

    def __str__(self):
        return f'Mineral {self.name}'

    def __repr__(self):
        return f'Mineral(id={self.id}, name={self.name}, description={self.description}, daily_value={self.daily_value}, \
        type_id={self.type_id}, type={self.type})'
