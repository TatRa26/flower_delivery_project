from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.db_utils import get_db_connection
from keyboards.main_menu import main_menu
from aiogram.fsm.context import FSMContext
from datetime import datetime
from handlers.quantity import user_cart

router = Router()


# Обработчик кнопки "Оформить заказ"
@router.callback_query(F.data == "checkout")
async def checkout(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    # Проверяем, есть ли товары в корзине
    if user_id not in user_cart or not user_cart[user_id]:
        await callback.message.answer("Ваша корзина пуста. Добавьте товары перед оформлением заказа.")
        return

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
    for item in user_cart[user_id]:
        cursor.execute(
            """
            INSERT INTO core_app_orderitem (order_id, product_id, quantity)
            VALUES (?, ?, ?)
            """,
            (order_id, item["product_id"], item["quantity"])
        )

    # Фиксируем изменения в базе данных
    connection.commit()
    connection.close()

    # Отправляем сообщение с подтверждением
    await callback.message.edit_text(
        "Заказ успешно создан. Теперь заполните данные для доставки с помощью команды /delivery.",
        reply_markup=main_menu()
    )


















