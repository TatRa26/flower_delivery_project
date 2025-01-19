import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Получение токена бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Получение путей и преобразование их в абсолютные
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Папка проекта
DB_PATH = os.path.join(BASE_DIR, os.getenv("DB_PATH"))
MEDIA_PATH = os.path.join(BASE_DIR, os.getenv("MEDIA_PATH"))
