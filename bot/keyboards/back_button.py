from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder

def back_button():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Назад", callback_data="back")
    return keyboard.as_markup()




