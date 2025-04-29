import os
import asyncio
import logging

from dotenv import load_dotenv

from app.handlers.user import rt
from app.database.models import engine, Base

from aiogram import Bot, Dispatcher

async def main():
    load_dotenv()
    dp = Dispatcher()
    bot = Bot(token=os.getenv('TOKEN'))

    @dp.startup()
    async def on_startup():
        await bot.delete_webhook(True)
        async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

        print('Бот запущен')
        
    dp.include_router(rt)
    await dp.start_polling(bot)
    print('Бот включен')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот отключен')