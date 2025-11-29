from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.base import Base


class BoilerInstructions(Base):
    __tablename__ = 'boiler_instructions'

    id: Mapped[int] = mapped_column(primary_key=True)
    model_id: Mapped[int] = mapped_column(ForeignKey('boiler_models.id'))
    doc_name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    file_id: Mapped[int | None] = mapped_column(ForeignKey("media_files.id"), nullable=True)
    access: Mapped[str] = mapped_column(String(20))

    file = relationship("MediaFile", back_populates="instructions")
    model = relationship("BoilerModel", back_populates="instructions")








