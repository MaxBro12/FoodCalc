from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from .mineral import Mineral
from .dish_products import Dishes_Association_Table


class Dish(Base):
    """
    Модель сохраненного пользователем блюда:
        - id: уникальный идентификатор
        - name: название блюда
        - description: описание блюда / рецепт в формате markdown
        - products: список продуктов, входящих в блюдо
        - is_verified: флаг, указывающий на верификацию блюда
        - likes: количество лайков блюда
        - search_index: индекс для поиска блюда

    Дополнительно:
        - minerals: список минералов, входящих в блюдо
    """
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    products: Mapped[list["Product"]] = relationship(
        "Product",
        secondary=Dishes_Association_Table,
        back_populates="dishes"
    )

    is_verified: Mapped[bool] = mapped_column(default=False)
    likes: Mapped[int] = mapped_column(default=0)
    search_index: Mapped[float] = mapped_column(default=0)

    added_by: Mapped[int]

    def __repr__(self):
        return f"<Dish(id={self.id}, name={self.name})>"

    def __str__(self):
        return f"Dish {self.name}"

    def minerals(self) -> tuple[Mineral, ...]:
        ans = []
        for product in self.products:
            ans.extend(product.minerals)
        return tuple(ans)
