from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from keyboards.main_menu import main_menu
from database.db_utils import get_db_connection
from json_utils import load_json, save_json  # Добавляем функции для работы с JSON

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    user_id = str(message.from_user.id)  # Преобразуем ID пользователя в строку
    first_name = message.from_user.first_name
    connection = get_db_connection()
    cursor = connection.cursor()

    # Загружаем данные о последних уведомленных статусах заказов из JSON
    notified_data = load_json()

    try:
        # Проверяем наличие пользователя в базе данных по его telegram_id
        cursor.execute("SELECT id FROM core_app_user WHERE telegram_id = ?", (user_id,))
        user = cursor.fetchone()

        if user:
            user_id_in_db = user[0]

            # Проверяем заказы пользователя
            cursor.execute(
                "SELECT id, status FROM core_app_order WHERE user_id = ?",
                (user_id_in_db,)
            )
            orders = cursor.fetchall()

            # Формируем сообщение о статусах заказов
            status_update_message = ""
            for order_id, status in orders:
                order_id = str(order_id)
                previous_status = notified_data.get(user_id, {}).get(order_id)

                if previous_status != status:
                    # Если статус изменился, добавляем сообщение и обновляем данные
                    status_update_message += f"Ваш статус заказа #{order_id} изменился на: '{status}'.\n"
                    if user_id not in notified_data:
                        notified_data[user_id] = {}
                    notified_data[user_id][order_id] = status

            # Сохраняем обновленные данные
            save_json(notified_data)

            # Формируем финальное сообщение
            text = f"Добро пожаловать в наш магазин цветов, {first_name}! 🌸\n"
            if status_update_message:
                text += status_update_message
            text += "Выберите действие:"

            await message.answer(text, reply_markup=main_menu())
        else:
            # Если пользователя нет, запрашиваем его username и email
            text = (
                "Мы не нашли ваш аккаунт.\n"
                "Введите ваш username и email, которые вы использовали на сайте, через запятую.\n"
                "Например: username, email@example.com"
            )
            await message.answer(text)
    finally:
        if connection:
            connection.close()


@router.message(F.text.contains(","))
async def handle_user_data(message: Message):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Получаем данные пользователя из сообщения
        user_data = message.text.split(",")
        if len(user_data) != 2:
            await message.answer("Пожалуйста, укажите username и email через запятую, например: username, email@example.com")
            return

        username = user_data[0].strip()
        email = user_data[1].strip()
        telegram_id = message.from_user.id

        # Проверяем, есть ли пользователь с указанным username и email
        cursor.execute(
            "SELECT id FROM core_app_user WHERE username = ? AND email = ?",
            (username, email),
        )
        user = cursor.fetchone()

        if user:
            # Обновляем telegram_id пользователя
            cursor.execute(
                "UPDATE core_app_user SET telegram_id = ? WHERE id = ?",
                (telegram_id, user[0]),
            )
            connection.commit()

            # Приветствие с выводом главного меню
            text = (
                f"Ваш аккаунт успешно найден и обновлен, {message.from_user.first_name}! 🌸\n"
                f"Выберите действие:"
            )
            await message.answer(text, reply_markup=main_menu())
        else:
            # Пользователь не найден — предлагаем регистрацию или выход
            text = (
                "Мы не нашли аккаунт с указанным username и email. Проверьте данные и попробуйте снова.\n\n"
                "Вы можете зарегистрироваться на сайте или выйти из бота:"
            )
            registration_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Регистрация", url="http://127.0.0.1:8000/register/")],
                    [InlineKeyboardButton(text="Выход", callback_data="exit_bot")]
                ]
            )
            await message.answer(text, reply_markup=registration_keyboard)
    finally:
        if connection:
            connection.close()


@router.callback_query(F.data == "exit_bot")
async def exit_bot(callback: CallbackQuery):
    await callback.message.edit_text("Вы покинули бот. Возвращайтесь, когда захотите! 👋")




