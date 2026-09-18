import asyncio
import os

from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, PhotoSize

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

token = os.getenv("TOKEN")

bot = Bot(token=token)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Я работаю 👋")

@dp.message(lambda message: message.photo)
async def photo_handler(message: Message):
    photo = message.photo[-1]

    await message.answer("Фото получил! 📸")

    file = await bot.get_file(photo.file_id)

    await bot.download_file(
        file.file_path,
        "input.jpg"
    )

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())