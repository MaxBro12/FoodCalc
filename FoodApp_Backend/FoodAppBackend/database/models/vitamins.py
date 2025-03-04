from ..base import Base
from sqlalchemy import Column, Integer, String


class Vitamins(Base):
    __tablename__ = 'vitamins'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
