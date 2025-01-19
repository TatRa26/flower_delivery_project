import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_PATH = r"C:\Users\Татьяна\PycharmProjects\flower_delivery_project\flower_delivery\db.sqlite3"
MEDIA_PATH = r"C:\Users\Татьяна\PycharmProjects\flower_delivery_project\flower_delivery\media"


