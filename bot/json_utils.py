import json
import os

# Путь к JSON-файлу, где хранятся данные о последних уведомленных статусах заказов
JSON_FILE = "notified_orders.json"

def load_json():
    """
    Загружает данные из JSON-файла.
    Если файл отсутствует, возвращает пустой словарь.
    Если файл повреждён, создаёт новый и возвращает пустой словарь.
    """
    if not os.path.exists(JSON_FILE):
        return {}

    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        # Если файл повреждён, создаём новый пустой
        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump({}, file, ensure_ascii=False, indent=4)
        return {}

def save_json(data):
    """
    Сохраняет данные в JSON-файл.
    Если файл отсутствует, создаёт его.
    """
    try:
        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        # Обрабатываем возможные ошибки записи в файл
        print(f"Ошибка при сохранении данных в файл {JSON_FILE}: {e}")
