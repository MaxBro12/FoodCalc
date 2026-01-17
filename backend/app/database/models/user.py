from datetime import datetime
from operator import is_
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    password: Mapped[str]
    is_admin: Mapped[bool]

    is_active: Mapped[bool] = mapped_column(default=True)
    unique: Mapped[str] = mapped_column(default='')
    refresh_token: Mapped[str] = mapped_column(default='')
    last_active: Mapped[datetime] = mapped_column(default=func.now())

    key_id: Mapped[int] = mapped_column(ForeignKey('access_keys.id'))
    key: Mapped['Key'] = relationship('Key', back_populates='users', lazy='selectin')

    products = relationship('Product', back_populates='added_by', lazy='selectin')

    def __str__(self):
        return f'User: {self.id} - {self.name} - {self.is_admin}'

    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, password={self.password}, is_admin={self.is_admin}, \
        last_active={self.last_active}, key_id={self.key_id})'
