from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Мои заказы", callback_data="my_orders")
    keyboard.button(text="Сделать заказ", callback_data="make_order")


    return keyboard.as_markup()




