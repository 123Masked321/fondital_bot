from typing import Optional
from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.base import Base


class BoilerError(Base):
    __tablename__ = 'boiler_errors'
    __table_args__ = (UniqueConstraint("brand_id", "type_id", "error_code", name="unique_boiler_error"))

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey('boiler_brands.id'))
    type_id: Mapped[int] = mapped_column(ForeignKey('boiler_types.id'))
    error_code: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    photo_file_id: Mapped[int | None] = mapped_column(ForeignKey("media_files.id"), nullable=True)

    photo_file = relationship("MediaFile", back_populates="errors")
    brand = relationship("BoilerBrand", back_populates="errors")
    boiler_type = relationship("BoilerType", back_populates="errors")








