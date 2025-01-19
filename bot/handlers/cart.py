from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.db_utils import get_db_connection
from keyboards.main_menu import main_menu
from aiogram.fsm.context import FSMContext
from datetime import datetime
from handlers.quantity import user_cart  # Импортируем корзину из quantity.py
from handlers.select_product import active_messages  # Импортируем активные сообщения

router = Router()

# Обработчик кнопки "Оформить заказ"
@router.callback_query(F.data == "checkout")
async def checkout(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    # Проверяем, есть ли товары в корзине
    if user_id not in user_cart or not user_cart[user_id]:
        await callback.message.answer("Ваша корзина пуста. Добавьте товары перед оформлением заказа.")
        return

    # Заблокировать кнопки, чтобы предотвратить повторное использование
    await callback.message.edit_reply_markup(reply_markup=None)

    # Создаем заказ в базе данных без данных для доставки
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM core_app_user WHERE telegram_id = ?", (user_id,)
    )
    user = cursor.fetchone()

    if not user:
        await callback.answer("Ошибка: пользователь не найден в базе данных.")
        connection.close()
        return

    user_db_id = user[0]

    # Создаем заказ в таблице core_app_order
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        """
        INSERT INTO core_app_order (
            user_id, status, order_date, delivery_address, delivery_date,
            recipient_name, recipient_phone
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (user_db_id, "pending", order_date, None, None, None, None)
    )
    order_id = cursor.lastrowid

    # Сохраняем товары из корзины в таблице core_app_orderitem
    cart_items_text = "Ваши товары в корзине:\n"
    total_order_price = 0
    for item in user_cart[user_id]:
        cursor.execute(
            """
            INSERT INTO core_app_orderitem (order_id, product_id, quantity)
            VALUES (?, ?, ?)
            """,
            (order_id, item["product_id"], item["quantity"])
        )
        cart_items_text += f"- {item['name']} (x{item['quantity']})\n"
        total_order_price += item["total_price"]

    # Фиксируем изменения в базе данных
    connection.commit()
    connection.close()

    # Очищаем корзину пользователя
    del user_cart[user_id]

    # Блокируем кнопку "Выбрать" для этого пользователя
    active_messages[user_id] = True

    # Отправляем сообщение с итогами заказа
    await callback.message.edit_text(
        f"✅ Заказ успешно создан. {cart_items_text}\nОбщая стоимость: {total_order_price}₽\n"
        "Теперь заполните данные для доставки с помощью команды /delivery."
    )

































