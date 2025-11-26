from sqlalchemy import Column, Integer, String, BigInteger, Boolean, ForeignKey, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    username: Mapped[str]
    full_name: Mapped[str]
    area: Mapped[str]
    city: Mapped[str]
    phone: Mapped[str]
    category: Mapped[str]
    role: Mapped[str] = mapped_column(default='user')
    is_processed: Mapped[bool] = mapped_column(Boolean, default=True)







