import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from aws.aws import S3Client
from db_handlers.database import *

load_dotenv()

TOKEN = getenv('TOKEN')

# настраиваем логирование и выводим в переменную для отдельного использования в нужных местах
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

db = Database()
s3 = S3Client(
    getenv("AWS_ACCESS_KEY"),
    getenv("AWS_SECRET_KEY"),
    getenv("AWS_REGION"),
    getenv("AWS_BUCKET")
)

# инициируем объект бота, передавая ему parse_mode=ParseMode.HTML по умолчанию
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# инициируем объект бота
dp = Dispatcher(storage=MemoryStorage())