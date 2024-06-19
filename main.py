import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from utils.config import TOKEN

loop = asyncio.get_event_loop()

client = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage(), loop=loop)

logging.basicConfig(level=logging.INFO)


async def main():
    from app.handlers import dp, router
    dp.include_router(router)
    await dp.start_polling(client)

if __name__ == '__main__':
    asyncio.run(main())


