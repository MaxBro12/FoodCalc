from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.database.models import MineralType


class Mineral(Base):
    __tablename__ = 'minerals'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    intake: Mapped[float]

    type_id: Mapped[int] = mapped_column(ForeignKey('mineral_types.id'))
    type: Mapped[MineralType] = relationship(MineralType, back_populates='minerals', lazy='selectin')

    def __str__(self):
        return f'Mineral {self.name} ({self.id}) - {self.intake} - {self.type}'

    def __repr__(self):
        return f'Mineral(id={self.id}, name={self.name}, description={self.description}, intake={self.intake}, \
        type_id={self.type_id}, type={self.type})'
