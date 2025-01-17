from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.db_utils import get_db_connection
from keyboards.main_menu import main_menu  # Клавиатура с главным меню

router = Router()

# Словарь для хранения данных доставки
user_delivery_info = {}

# Состояния для заполнения данных доставки
class DeliveryState(StatesGroup):
    date_time = State()
    address = State()
    recipient_name = State()
    recipient_phone = State()

# Начало команды /delivery
@router.message(F.text == "/delivery")
async def start_delivery(message: Message, state: FSMContext):
    await message.answer("Введите дату и время доставки (например, 2025-01-16 14:30):")
    await state.set_state(DeliveryState.date_time)

# Получение даты и времени доставки
@router.message(DeliveryState.date_time)
async def enter_date_time(message: Message, state: FSMContext):
    # Сохраняем дату и время доставки
    await state.update_data(date_time=message.text)
    await message.answer("Введите адрес доставки (без запятых):")
    await state.set_state(DeliveryState.address)

# Получение адреса доставки
@router.message(DeliveryState.address)
async def enter_address(message: Message, state: FSMContext):
    # Расширенная валидация адреса
    address = message.text.strip()
    if "," in address or len(address) < 5:
        await message.answer("Адрес не должен содержать запятые и должен быть не короче 5 символов. Попробуйте снова:")
        return

    await state.update_data(address=address)
    await message.answer("Введите имя получателя (только буквы, минимум 2 символа):")
    await state.set_state(DeliveryState.recipient_name)

# Получение имени получателя
@router.message(DeliveryState.recipient_name)
async def enter_recipient_name(message: Message, state: FSMContext):
    # Расширенная валидация имени
    name = message.text.strip()
    if not name.isalpha() or len(name) < 2:
        await message.answer("Имя должно содержать только буквы и быть не короче 2 символов. Попробуйте снова:")
        return

    await state.update_data(recipient_name=name)
    await message.answer("Введите номер телефона получателя (например, +1234567890):")
    await state.set_state(DeliveryState.recipient_phone)

# Получение номера телефона получателя
@router.message(DeliveryState.recipient_phone)
async def enter_recipient_phone(message: Message, state: FSMContext):
    # Простая валидация телефона
    phone = message.text.strip()
    if not phone.startswith("+") or not phone[1:].isdigit() or len(phone) < 10:
        await message.answer("Введите корректный номер телефона в формате +1234567890:")
        return

    await state.update_data(recipient_phone=phone)

    user_id = message.from_user.id
    data = await state.get_data()

    # Сохраняем данные в словарь user_delivery_info
    user_delivery_info[user_id] = {
        "date_time": data["date_time"],
        "address": data["address"],
        "recipient_name": data["recipient_name"],
        "recipient_phone": data["recipient_phone"]
    }

    # Записываем данные для доставки в базу данных
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM core_app_user WHERE telegram_id = ?", (user_id,)
    )
    user = cursor.fetchone()

    if user:
        user_db_id = user[0]

        # Обновляем заказ с данными для доставки
        cursor.execute(
            """
            UPDATE core_app_order
            SET delivery_date = ?, delivery_address = ?, recipient_name = ?, recipient_phone = ?
            WHERE user_id = ? AND status = 'pending'
            """,
            (data["date_time"], data["address"], data["recipient_name"], data["recipient_phone"], user_db_id)
        )
        connection.commit()

    connection.close()

    await message.answer(
        "Данные для доставки успешно сохранены! Теперь ваш заказ готов. Возвращаемся в главное меню.",
        reply_markup=main_menu()
    )

    await state.clear()


