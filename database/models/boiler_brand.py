from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base


class BoilerBrand(Base):
    __tablename__ = 'boiler_brands'

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    photo_path_from_s3: Mapped[Optional[str]] = mapped_column(nullable=True)
    photo_path_telegram_id: Mapped[Optional[str]] = mapped_column(nullable=True)

    models = relationship("BoilerModel", back_populates="brand")
    errors = relationship("BoilerError", back_populates="brand")








