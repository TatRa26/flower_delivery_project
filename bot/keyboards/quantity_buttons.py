from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton


from datetime import datetime
import sqlite3




# Создание кнопок для выбора количества
def create_quantity_buttons(quantity):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="-", callback_data="decrease_quantity"),
                InlineKeyboardButton(text=f"Количество: {quantity}", callback_data="current_quantity"),
                InlineKeyboardButton(text="+", callback_data="increase_quantity"),
            ],
            [InlineKeyboardButton(text="Принять", callback_data="accept_quantity")],
        ]
    )
    return keyboard


