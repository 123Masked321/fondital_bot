from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base


class MediaFile(Base):
    __tablename__ = 'media_files'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_file_id: Mapped[Optional[str]] = mapped_column(nullable=True)
    telegram_unique_id: Mapped[Optional[str]] = mapped_column(unique=True, nullable=True)
    s3_key: Mapped[Optional[str]] = mapped_column(nullable=True)
    sha256: Mapped[Optional[str]] = mapped_column(unique=True, nullable=True)
    content_type: Mapped[Optional[str]] = mapped_column(nullable=True)
    size: Mapped[Optional[int]] = mapped_column(nullable=True)

    brands = relationship("BoilerBrand", back_populates="photo_file")
    types = relationship("BoilerType", back_populates="photo_file")
    models = relationship("BoilerModel", back_populates="photo_file")
    errors = relationship("BoilerError", back_populates="photo_file")
    instructions = relationship("BoilerInstructions", back_populates="file")
    start = relationship("StartScreen", back_populates="photo_file")