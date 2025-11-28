from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class ProductMineral(Base):
    __tablename__ = 'products_minerals'

    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), primary_key=True)
    mineral_id: Mapped[int] = mapped_column(ForeignKey('minerals.id'), primary_key=True)
    content: Mapped[float] = mapped_column(nullable=False)

    product: Mapped['Product'] = relationship(back_populates='minerals')
    mineral: Mapped['Mineral'] = relationship(back_populates='products')
