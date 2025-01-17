import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import start, orders, products, back, select_product, cart, quantity
from handlers.delivery import router as delivery_router
from aiogram.fsm.storage.memory import MemoryStorage


bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Подключение роутеров
dp.include_router(start.router)
dp.include_router(orders.router)
dp.include_router(products.router)
dp.include_router(back.router)
dp.include_router(select_product.router)
dp.include_router(quantity.router)
dp.include_router(cart.router)
dp.include_router(delivery_router)



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())














