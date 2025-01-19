from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.db_utils import get_db_connection  # Функция для подключения к базе данных
from keyboards.quantity_buttons import create_quantity_buttons  # Функция для создания кнопок "+", "-"
from keyboards.main_menu import main_menu  # Клавиатура с главным меню
from datetime import datetime  # Для сохранения даты заказа
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Глобальные переменные
user_quantities = {}  # Хранит выбранные пользователем данные (товар и количество)
user_cart = {}  # Хранит данные корзины пользователей

# Инициализация роутера
router = Router()

# Обработчик кнопки "+"
@router.callback_query(F.data == "increase_quantity")
async def increase_quantity(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Если пользователь уже начал выбор количества
    if user_id in user_quantities:
        user_quantities[user_id]["quantity"] += 1
        quantity = user_quantities[user_id]["quantity"]

        # Обновляем клавиатуру
        await callback.message.edit_reply_markup(
            reply_markup=create_quantity_buttons(quantity)
        )
    else:
        await callback.answer("Ошибка: данные не найдены.")

# Обработчик кнопки "-"
@router.callback_query(F.data == "decrease_quantity")
async def decrease_quantity(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Если пользователь уже начал выбор количества
    if user_id in user_quantities:
        if user_quantities[user_id]["quantity"] > 1:
            user_quantities[user_id]["quantity"] -= 1
        quantity = user_quantities[user_id]["quantity"]

        # Обновляем клавиатуру
        await callback.message.edit_reply_markup(
            reply_markup=create_quantity_buttons(quantity)
        )
    else:
        await callback.answer("Ошибка: данные не найдены.")

# Обработчик кнопки "Принять количество"
@router.callback_query(F.data == "accept_quantity")
async def accept_quantity(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = user_quantities.pop(user_id, None)

    if user_data:
        product_id = user_data["product_id"]
        quantity = user_data["quantity"]

        # Получаем данные о товаре из базы данных
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT name, price FROM core_app_product WHERE id = ?", (product_id,)
        )
        product = cursor.fetchone()
        connection.close()

        if product:
            name, price = product
            total_price = price * quantity

            # Добавляем товар в корзину
            if user_id not in user_cart:
                user_cart[user_id] = []
            user_cart[user_id].append({
                "product_id": product_id,
                "name": name,
                "price": price,
                "quantity": quantity,
                "total_price": total_price
            })

            # Обновляем сообщение с кнопками
            await callback.message.edit_text(
            f"Товар: {name}\n"
            f"Количество: {quantity} шт.\n"
            f"Цена за единицу: {price}₽\n"
            f"Общая стоимость: {total_price}₽\n"
            "Вы можете выбрать ещё товар перед тем, как нажать 'Оформить заказ'.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Оформить заказ", callback_data="checkout")],
                    [InlineKeyboardButton(text="Удалить товар", callback_data="delete_item")],
                    [InlineKeyboardButton(text="Назад", callback_data="back")]
                ]
            )
        )
        else:
            await callback.message.answer("Ошибка: товар не найден.")
    else:
        await callback.answer("Ошибка: данные не найдены.")

# Добавление обработчика кнопки "Удалить товар"
@router.callback_query(F.data == "delete_item")
async def delete_item(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Проверяем, есть ли товары в корзине
    if user_id in user_cart and user_cart[user_id]:
        # Удаляем последний добавленный товар (пример логики, можно изменить)
        deleted_item = user_cart[user_id].pop(-1)

        if not user_cart[user_id]:
            # Если корзина пуста после удаления
            del user_cart[user_id]

        await callback.message.edit_text(
            f"Товар '{deleted_item['name']}' удален из корзины.\n"
            "Вы можете выбрать другой товар в каталоге.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Оформить заказ", callback_data="checkout")],
                    [InlineKeyboardButton(text="Назад", callback_data="back")]
                ]
            )
        )
    else:
        await callback.answer("Корзина пуста или данные не найдены.")

# Функция для установки начальных данных (вызвать при выборе товара)
def set_user_quantity(user_id: int, product_id: int):
    user_quantities[user_id] = {"product_id": product_id, "quantity": 1}



