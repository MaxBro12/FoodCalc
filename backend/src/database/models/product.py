from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.database import Base
from .dish_products import Dishes_Association_Table


class Product(Base):
    """
    Модель продукта.
    - `id`: уникальный идентификатор продукта или barcode
    - `name`: название продукта
    - `description`: описание продукта
    - `calories_per_100g`: количество калорий на 100г продукта
    - `proteins_per_100g`: количество белков на 100г продукта
    - `fats_per_100g`: количество жиров на 100г продукта
    - `carbs_per_100g`: количество углеводов на 100г продукта
    - `fiber_per_100g`: количество волокон на 100г продукта
    - `sugar_per_100g`: количество сахара на 100г продукта
    - `added_by`: идентификатор пользователя, добавившего продукт
    - `is_verified`: флаг верификации администратором продукта
    - `likes`: количество лайков продукта
    - `search_index`: поисковой индекс продукта - чем больше, тем чаще ищут. Максимальное значение - 100
    - `created_at`: дата и время создания продукта
    - `updated_at`: дата и время последнего обновления продукта
    """

    __tablename__ = 'products'

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(default='Описание не указано')

    calories_per_100g: Mapped[float] = mapped_column(default=0)
    proteins_per_100g: Mapped[float] = mapped_column(default=0)
    fats_per_100g: Mapped[float] = mapped_column(default=0)
    carbs_per_100g: Mapped[float] = mapped_column(default=0)
    fiber_per_100g: Mapped[float] = mapped_column(default=0)
    sugar_per_100g: Mapped[float] = mapped_column(default=0)

    added_by: Mapped[int]
    is_verified: Mapped[bool] = mapped_column(default=False)
    likes: Mapped[int] = mapped_column(default=0)
    search_index: Mapped[float] = mapped_column(default=0)

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now())

    minerals: Mapped[list["ProductMineral"]] = relationship(
        back_populates='product',
        lazy='selectin',
        cascade='all, delete-orphan'
    )
    dishes: Mapped[list["Dish"]] = relationship(
        "Dish",
        secondary=Dishes_Association_Table,
        back_populates="products"
    )
