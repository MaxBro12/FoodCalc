from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Key(Base):
    __tablename__ = 'access_keys'

    id: Mapped[int] = mapped_column(primary_key=True)
    hash: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    users: Mapped[List['User']] = relationship('User', back_populates='key')

    def __str__(self):
        return f'Key: {self.id} - {self.hash} is admin {self.is_admin}'

    def __repr__(self):
        return f'Key(id={self.id}, hash={self.hash}, is_admin={self.is_admin})'
