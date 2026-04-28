from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from .mineral import Mineral


class Dish(Base):
    """
    Модель сохраненного пользователем блюда:
        - id: уникальный идентификатор
        - name: название блюда
        - description: описание блюда / рецепт в формате markdown
        - products: список продуктов, входящих в блюдо

    Дополнительно:
        - minerals: список минералов, входящих в блюдо
    """
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    products: Mapped[list["Product"]] = relationship("Product", back_populates="dishes")

    added_by: Mapped[int]

    def __repr__(self):
        return f"<Dish(id={self.id}, name={self.name})>"

    def __str__(self):
        return self.name

    def minerals(self) -> tuple[Mineral, ...]:
        ans = []
        for product in self.products:
            ans.extend(product.minerals)
        return tuple(ans)
