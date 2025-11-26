from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base


class BoilerInstructions(Base):
    __tablename__ = 'boiler_instructions'

    id: Mapped[int] = mapped_column(primary_key=True)
    model_id: Mapped[int] = mapped_column(ForeignKey('boiler_models.id'))
    doc_name: Mapped[str]
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    doc_path_from_s3: Mapped[str]
    doc_path_telegram_id: Mapped[str]
    access: Mapped[str] = mapped_column(String(20))

    model = relationship("BoilerModel", back_populates="instructions")








