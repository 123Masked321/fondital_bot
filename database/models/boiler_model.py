from typing import Optional

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base


class BoilerModel(Base):
    __tablename__ = 'boiler_models'
    __table_args__ = (UniqueConstraint("brand_id", "type_id", "model_name", name="unique_boiler_model"))

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey('boiler_brands.id'))
    type_id: Mapped[int] = mapped_column(ForeignKey('boiler_types.id'))
    model_name: Mapped[str] = mapped_column(String(128))
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    photo_path_from_s3: Mapped[Optional[str]] = mapped_column(nullable=True)
    photo_path_telegram_id: Mapped[Optional[str]] = mapped_column(nullable=True)

    brand = relationship("BoilerBrand", back_populates="models")
    type = relationship("BoilerType", back_populates="models")

    instructions = relationship("BoilerInstructions", back_populates="model")







