from typing import Optional

from sqlalchemy import BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from database.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)

    username: Mapped[Optional[str]] = mapped_column(nullable=True)
    full_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    area: Mapped[Optional[str]] = mapped_column(nullable=True)
    city: Mapped[Optional[str]] = mapped_column(nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(nullable=True)
    category: Mapped[Optional[str]] = mapped_column(nullable=True)

    role: Mapped[str] = mapped_column(default='user')
    is_processed: Mapped[bool] = mapped_column(Boolean, default=True)







