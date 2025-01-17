from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.db_utils import get_db_connection
from keyboards.back_button import back_button
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(F.data == "my_orders")
async def show_orders(callback: CallbackQuery):
    user_id = callback.from_user.id
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id, username, email, address FROM core_app_user WHERE telegram_id = ?", (user_id,)
        )
        user = cursor.fetchone()

        if user:
            user_id, username, email, address = user
            orders = cursor.execute(
                """
                SELECT o.id AS order_id, o.order_date, o.status, p.name, oi.quantity, p.price
                FROM core_app_order o
                JOIN core_app_orderitem oi ON o.id = oi.order_id
                JOIN core_app_product p ON oi.product_id = p.id
                WHERE o.user_id = ?
                """,
                (user_id,),
            ).fetchall()

            if orders:
                order_text = f"Ваш адрес доставки: {address if address else 'Не указан'}\n\n"
                current_order_id = None
                for order in orders:
                    order_id, order_date, status, product_name, quantity, price = order
                    if order_id != current_order_id:
                        if current_order_id is not None:
                            order_text += "\n"
                        order_text += f"Заказ #{order_id} (Дата: {order_date}, Статус: {status}):\n"
                        current_order_id = order_id
                    order_text += f" - {product_name}: {quantity} шт. × {price}₽\n"

                await callback.message.edit_text(
                    f"Ваши заказы:\n\n{order_text}", reply_markup=back_button()
                )
            else:
                await callback.message.edit_text(
                    "У вас пока нет заказов.", reply_markup=back_button()
                )
        else:
            await callback.message.edit_text(
                "Мы не нашли ваш аккаунт.\nВведите ваш username и email, "
                "которые вы использовали на сайте.",
                reply_markup=back_button(),
            )
    finally:
        if connection:
            connection.close()










