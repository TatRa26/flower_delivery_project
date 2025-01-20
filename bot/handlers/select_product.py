from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.quantity_buttons import create_quantity_buttons
from handlers.quantity import set_user_quantity
from database.db_utils import get_db_connection
from aiogram.types import CallbackQuery, FSInputFile
import os
from config import MEDIA_PATH

router = Router()

# Словарь для хранения количества (на уровне пользователя)
user_quantities = {}

# Словарь для отслеживания активных сообщений (кнопок)
active_messages = {}


# Обработчик кнопки "Выбрать"
@router.callback_query(F.data.startswith("select_product:"))
async def select_product(callback: CallbackQuery):
    product_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    # Проверяем, заблокирована ли кнопка "Выбрать" для этого пользователя
    if user_id in active_messages and active_messages[user_id]:
        await callback.answer("Вы уже оформили заказ. Кнопка заблокирована.")
        return

    # Устанавливаем начальное количество для выбранного товара
    set_user_quantity(user_id=user_id, product_id=product_id)

    # Получаем данные о товаре из базы данных
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT name, price, image FROM core_app_product WHERE id = ?", (product_id,)
    )
    product = cursor.fetchone()
    connection.close()

    if product:
        name, price, image = product
        image_path = os.path.join(MEDIA_PATH, image)

        # Удаляем текущее сообщение
        await callback.message.delete()

        # Отправляем изображение товара
        if os.path.exists(image_path):
            photo = FSInputFile(image_path)
            await callback.message.answer_photo(
                photo=photo,
                caption=f"{name} - {price}₽"
            )
        else:
            await callback.message.answer(
                f"⚠️ Нет изображения для товара: {name} - {price}₽"
            )

        # Отправляем сообщение с кнопками для выбора количества
        await callback.message.answer(
            "Выберите количество товара:",
            reply_markup=create_quantity_buttons(1)
        )
    else:
        await callback.message.answer("Товар не найден.")












