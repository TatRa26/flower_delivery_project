from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from database.db_utils import get_db_connection
from keyboards.back_button import back_button
from keyboards.product_buttons import create_product_buttons
import os

router = Router()

@router.callback_query(F.data == "make_order")
async def make_order(callback: CallbackQuery):
    """Обработка команды 'Сделать заказ'. Показывает товары из базы данных."""
    connection = get_db_connection()
    cursor = connection.cursor()

    # Получение списка товаров из базы данных
    products = cursor.execute("SELECT id, name, price, image FROM core_app_product").fetchall()
    connection.close()

    if products:
        await callback.message.edit_text("Выберите товар из каталога:")

        # Отправляем изображения товаров с кнопками
        for product in products:
            product_id, name, price, image = product
            caption = f"{name} - {price}₽"
            image_path = os.path.join(
                "C:/Users/Татьяна/PycharmProjects/flower_delivery_project/flower_delivery/media",
                image
            )

            # Проверяем существование изображения
            if os.path.exists(image_path):
                try:
                    photo = FSInputFile(image_path)
                    await callback.message.answer_photo(
                        photo=photo,
                        caption=caption,
                        reply_markup=create_product_buttons(product_id)
                    )
                except Exception as e:
                    await callback.message.answer(
                        f"⚠️ Ошибка отображения для: {caption}",
                        reply_markup=create_product_buttons(product_id)
                    )
            else:
                await callback.message.answer(
                    f"⚠️ Нет изображения для: {caption}",
                    reply_markup=create_product_buttons(product_id)
                )
    else:
        # Если товаров нет
        await callback.message.edit_text(
            "К сожалению, в данный момент нет доступных товаров.",
            reply_markup=back_button()
        )


