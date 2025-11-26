from sqlalchemy import Column, Integer, String, BigInteger, Boolean, ForeignKey, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base


class BoilerBrand(Base):
    __tablename__ = 'boiler_brands'

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    description: Mapped[str]
    photo_path_from_s3: Mapped[str]
    photo_path_telegram_id: Mapped[str]

    models = relationship("BoilerModel", back_populates="brand")
    errors = relationship("BoilerError", back_populates="brand")


class BoilerType(Base):
    __tablename__ = 'boiler_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    description: Mapped[str]
    photo_path_from_s3: Mapped[str]
    photo_path_telegram_id: Mapped[str]

    models = relationship("BoilerModel", back_populates="type")
    errors = relationship("BoilerError", back_populates="type")


class BoilerError(Base):
    __tablename__ = 'boiler_errors'
    __table_args__ = {UniqueConstraint("brand_id", "type_id", "error_code", name="unique_boiler_error")}

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey('boiler_brands.id'))
    type_id: Mapped[int] = mapped_column(ForeignKey('boiler_types.id'))
    error_code: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str]
    photo_path_from_s3: Mapped[str]
    photo_path_telegram_id: Mapped[str]

    brand = relationship("BoilerBrand", back_populates="errors")
    type = relationship("BoilerType", back_populates="errors")


class BoilerModel(Base):
    __tablename__ = 'boiler_models'
    __table_args__ = (UniqueConstraint("brand_id", "type_id", "model_name", name="unique_boiler_model"))

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey('boiler_brands.id'))
    type_id: Mapped[int] = mapped_column(ForeignKey('boiler_types.id'))
    model_name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str]
    photo_path_from_s3: Mapped[str]
    photo_path_telegram_id: Mapped[str]

    brand = relationship("BoilerBrand", back_populates="models")
    type = relationship("BoilerType", back_populates="models")

    instructions = relationship("BoilerInstructions", back_populates="model")


class BoilerInstructions(Base):
    __tablename__ = 'boiler_instructions'

    id: Mapped[int] = mapped_column(primary_key=True)
    model_id: Mapped[int] = mapped_column(ForeignKey('boiler_models.id'))
    doc_name: Mapped[str]
    description: Mapped[str]
    doc_path_from_s3: Mapped[str]
    doc_path_telegram_id: Mapped[str]
    access: Mapped[str] = mapped_column(String(20))

    model = relationship("BoilerModel", back_populates="instructions")


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







