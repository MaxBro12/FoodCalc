from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.database import Base
from .dish_products import Dishes_Association_Table


class Product(Base):
    """
    Модель продукта.
    - `id`: уникальный идентификатор продукта
    - `name`: название продукта
    - `description`: описание продукта
    - `added_by`: идентификатор пользователя, добавившего продукт
    - `is_verified`: флаг верификации администратором продукта
    - `likes`: количество лайков продукта
    - `search_index`: поисковой индекс продукта - чем больше, тем чаще ищут. Максимальное значение - 100
    """

    __tablename__ = 'products'

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(default='Описание не указано')

    added_by: Mapped[int]
    is_verified: Mapped[bool] = mapped_column(default=False)
    likes: Mapped[int] = mapped_column(default=0)
    search_index: Mapped[float] = mapped_column(default=0)

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
