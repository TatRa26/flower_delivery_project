from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from database.db_utils import get_db_connection
from keyboards.back_button import back_button
import os
from config import MEDIA_PATH

router = Router()

@router.callback_query(F.data == "my_orders")
async def show_orders(callback: CallbackQuery):
    user_id = callback.from_user.id
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id, username, email FROM core_app_user WHERE telegram_id = ?", (user_id,)
        )
        user = cursor.fetchone()

        if user:
            user_id, username, email = user
            orders = cursor.execute(
                """
                SELECT o.id AS order_id, o.delivery_date, o.delivery_address, o.status, 
                       p.name, oi.quantity, p.price, p.image
                FROM core_app_order o
                JOIN core_app_orderitem oi ON o.id = oi.order_id
                JOIN core_app_product p ON oi.product_id = p.id
                WHERE o.user_id = ?
                """,
                (user_id,),
            ).fetchall()

            if orders:
                current_order_id = None
                total_price = 0

                for index, order in enumerate(orders):
                    order_id, delivery_date, delivery_address, status, product_name, quantity, price, image = order

                    # Если новый заказ, обрабатываем вывод информации о предыдущем
                    if order_id != current_order_id:
                        if current_order_id is not None:
                            # Выводим информацию о предыдущем заказе
                            await callback.message.answer(
                                f"Заказ #{current_order_id}\n"
                                f"Дата доставки: {delivery_date}\n"
                                f"Адрес доставки: {delivery_address}\n"
                                f"Статус: {status}\n"
                                f"Общая стоимость: {total_price}₽"
                            )
                        # Сбрасываем данные для нового заказа
                        current_order_id = order_id
                        total_price = 0

                    # Суммируем общую стоимость для заказа
                    total_price += quantity * price

                    # Отправляем фото товара
                    if image:
                        image_path = os.path.join(MEDIA_PATH, image)

                        if os.path.exists(image_path):
                            photo = FSInputFile(image_path)
                            try:
                                await callback.message.answer_photo(
                                    photo=photo,
                                    caption=f"{product_name}: {quantity} шт. × {price}₽ (Заказ #{order_id})"
                                )
                            except Exception as e:
                                await callback.message.answer("Ошибка при отправке изображения.")
                                print(f"Ошибка отправки фото {image_path}: {e}")
                        else:
                            print(f"Изображение для товара {product_name} не найдено.")

                # Выводим информацию о последнем заказе с кнопкой «Назад»
                await callback.message.answer(
                    f"Заказ #{current_order_id}\n"
                    f"Дата доставки: {delivery_date}\n"
                    f"Адрес доставки: {delivery_address}\n"
                    f"Статус: {status}\n"
                    f"Общая стоимость: {total_price}₽",
                    reply_markup=back_button()  # Кнопка «Назад» только под последним заказом
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




















