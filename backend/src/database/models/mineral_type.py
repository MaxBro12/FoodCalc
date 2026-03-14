from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class MineralType(Base):
    __tablename__ = 'mineral_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]

    minerals: Mapped[List['Mineral']] = relationship('Mineral', back_populates='type')

    def __str__(self):
        return f'Mineral Type: {self.name} - {self.description}'

    def __repr__(self):
        return f'MineralType(id={self.id}, name={self.name}, description={self.description})'
