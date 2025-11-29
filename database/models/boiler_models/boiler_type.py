from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.base import Base


class BoilerType(Base):
    __tablename__ = 'boiler_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    photo_file_id: Mapped[int | None] = mapped_column(ForeignKey("media_files.id"), nullable=True)

    photo_file = relationship("MediaFile", back_populates="types")
    models = relationship("BoilerModel", back_populates="boiler_type")
    errors = relationship("BoilerError", back_populates="boiler_type")






