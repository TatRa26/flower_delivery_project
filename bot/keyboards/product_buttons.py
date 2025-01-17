from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Создание кнопок для товара
def create_product_buttons(product_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Выбрать", callback_data=f"select_product:{product_id}")],
            [InlineKeyboardButton(text="Назад", callback_data="back")]
        ]
    )
    return keyboard