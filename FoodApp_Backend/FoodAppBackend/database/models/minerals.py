from ..base import Base
from sqlalchemy import Column, Integer, String


class Minerals(Base):
    __tablename__ = 'minerals'

    id = Column(Integer, primary_key=True)
    name = Column(String(5), nullable=False)
    description = Column(String(255), nullable=False)
