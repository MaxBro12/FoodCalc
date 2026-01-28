from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Key(Base):
    __tablename__ = 'access_keys'

    id: Mapped[int] = mapped_column(primary_key=True)
    hash: Mapped[str] = mapped_column(nullable=False, unique=True)
    app_name: Mapped[str] = mapped_column(nullable=False)

    users: Mapped[List['User']] = relationship('User', back_populates='key')

    def __str__(self):
        return f'Key: {self.id} - {self.app_name}'

    def __repr__(self):
        return f'Key(id={self.id}, hash={self.hash}, app_name={self.app_name})'
