from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from keyboards.main_menu import main_menu
from database.db_utils import get_db_connection

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Проверяем наличие пользователя в базе данных по его telegram_id
        cursor.execute("SELECT username, email FROM core_app_user WHERE telegram_id = ?", (user_id,))
        user = cursor.fetchone()

        if user:
            # Пользователь найден
            text = (
                f"Добро пожаловать в наш магазин цветов, {first_name}! 🌸\n"
                f"Выберите действие:"
            )
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



