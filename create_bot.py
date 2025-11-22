import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config.settings import settings
from aws.s3 import S3Client


# ---------- logger ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ---------- s3 ----------
s3 = S3Client(
    settings.AWS_ACCESS_KEY,
    settings.AWS_SECRET_KEY,
    settings.AWS_REGION,
    settings.AWS_BUCKET
)

# ---------- bot ----------
bot = Bot(
    token=settings.TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# ---------- dispatcher ----------
dp = Dispatcher(storage=MemoryStorage())
