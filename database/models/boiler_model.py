from typing import Optional
from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.base import Base


class BoilerModel(Base):
    __tablename__ = 'boiler_models'
    __table_args__ = (UniqueConstraint("brand_id", "type_id", "model_name", name="unique_boiler_model"))

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey('boiler_brands.id'))
    type_id: Mapped[int] = mapped_column(ForeignKey('boiler_types.id'))
    model_name: Mapped[str] = mapped_column(String(128))
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    photo_file_id: Mapped[int | None] = mapped_column(ForeignKey("media_files.id"), nullable=True)

    photo_file = relationship("MediaFile", back_populates="models")
    brand = relationship("BoilerBrand", back_populates="models")
    boiler_type = relationship("BoilerType", back_populates="models")

    instructions = relationship("BoilerInstructions", back_populates="model")







