from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    TOKEN: str

    AWS_ACCESS_KEY: str | None = None
    AWS_SECRET_KEY: str | None = None
    AWS_BUCKET: str | None = None
    AWS_REGION: str | None = None

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}"
            f"/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
