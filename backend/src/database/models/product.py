from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.database import Base


class Product(Base):
    """
    Модель продукта.
    - `id`: уникальный идентификатор продукта
    - `name`: название продукта
    - `description`: описание продукта
    - `added_by`: идентификатор пользователя, добавившего продукт
    - `minerals`: список минералов, входящих в продукт
    - `search_index`: поисковой индекс продукта - чем больше, тем чаще ищут. Максимальное значение - 100
    """

    __tablename__ = 'products'

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(default='Описание не указано')

    added_by: Mapped[int]

    minerals: Mapped[list["ProductMineral"]] = relationship(
        back_populates='product',
        lazy='selectin',
        cascade='all, delete-orphan'
    )
    dishes: Mapped[list["Dish"]] = relationship("Dish", back_populates="products")

    search_index: Mapped[float] = mapped_column(default=0)
