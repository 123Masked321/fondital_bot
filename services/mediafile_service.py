from typing import Optional

from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from aws.s3 import S3Client
from database.models.mediafiles import MediaFile


class MediaFileService:
    def __init__(self, session: AsyncSession, s3: S3Client) -> None:
        self.session = session
        self.s3 = s3

    @staticmethod
    async def _extract_telegram_meta(
            message: Message
    ) -> tuple[str, str, str, Optional[str], Optional[str]]:
        """
        Определяем, что прилетело: photo или document,
        и достаём нужные поля.
        """
        if message.photo:
            kind: str = "photo"
            p: PhotoSize = message.photo[-1]
            telegram_file_id = p.file_id
            telegram_unique_id = p.file_unique_id
            content_type = "image/jpeg"
        elif message.document:
            kind = "document"
            d: Document = message.document
            telegram_file_id = d.file_id
            telegram_unique_id = d.file_unique_id
            content_type = d.mime_type
        else:
            raise ValueError("Message must contain photo or document")

        return kind, telegram_file_id, telegram_unique_id, content_type, original_filename

    async def get_or_create_mediafile(self, message: Message) -> None:
        telegram_file_id, telegram_unique_id, filename, mime_type = self._extract_telegram_fields(message)