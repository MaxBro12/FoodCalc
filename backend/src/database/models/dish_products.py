from sqlalchemy import Table, Column, Integer, ForeignKey
from src.database import Base


Dishes_Association_Table = Table(
    "dishes_products",
    Base.metadata,
    Column("dish_id", Integer, ForeignKey("dishes.id")),
    Column("product_id", Integer, ForeignKey("products.id")),
)
