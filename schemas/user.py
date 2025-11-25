from typing import Optional, Literal

from pydantic import BaseModel, field_validator


class UserBase(BaseModel):
    full_name: Optional[str] = None
    area: Optional[str] = None
    city: Optional[str] = None
    category: Optional[str] = None
    phone: Optional[str] = None
    role: Literal["user", "admin", "spec"]
    is_processed: bool = True

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: Optional[str]):
        if value and not value.startswith("+"):
            raise ValueError("Phone must start with +")
        return value


class UserCreate(UserBase):
    telegram_id: int
    username: Optional[str] = None

