from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.database import Base


class ProductMineral(Base):
    """
    Модель связи продукта и минерала.
    - `product_id`: идентификатор продукта
    - `mineral_id`: идентификатор минерала
    - `amount_per_100g`: содержание Минерала в продукте в милиграммах
    - `product`: связь с моделью продукта
    - `mineral`: связь с моделью минерала
    """

    __tablename__ = 'products_minerals'

    product_id: Mapped[str] = mapped_column(ForeignKey('products.id'), primary_key=True)
    mineral_id: Mapped[int] = mapped_column(ForeignKey('minerals.id'), primary_key=True)
    amount_per_100g: Mapped[float] = mapped_column(nullable=False)  # Содержание минерала в продукте в милиграммах

    product: Mapped['Product'] = relationship(back_populates='minerals', lazy='joined')
    mineral: Mapped['Mineral'] = relationship(back_populates='products', lazy='joined')
