import asyncio
from aiogram.client.default import DefaultBotProperties
import os
from aiogram import Bot, Dispatcher
from app.handlers import router
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

async def main():
    dp.include_router(router)
    # комбинация ctrl+/ а то ты вечно забываешь
    await dp.start_polling(bot)

if __name__=='__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')