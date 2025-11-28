from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base


class StartScreen(Base):
    __tablename__ = 'start_screen'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    photo_file_id: Mapped[int | None] = mapped_column(ForeignKey("media_files.id"), nullable=True)

    photo_file = relationship("MediaFile", back_populates="start")







