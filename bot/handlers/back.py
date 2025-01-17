from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.main_menu import main_menu

router = Router()


# Обработчик кнопки "Назад"
@router.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery):
    # Удаляем текущее сообщение
    await callback.message.delete()

    # Отправляем новое сообщение с начальным меню
    await callback.message.answer(
        "Добро пожаловать в наш магазин цветов! 🌸\nВыберите действие:",
        reply_markup=main_menu(),
    )
