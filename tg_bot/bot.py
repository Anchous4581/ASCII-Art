# bot.py
import asyncio
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ascii_core.converter import convert
from ascii_core.renderer import render_ascii_to_image
from ascii_core.config import min_width, max_width, default_width


load_dotenv(
    PROJECT_ROOT / ".env"
)

token = os.getenv("TOKEN")
user_widths = {}

bot = Bot(token=token)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Привет! 👋\n\n"
        "Я превращаю изображения в ASCII-art 🗿\n\n"
        "📸 **Просто отправь мне изображение** — я превращу его в ASCII.\n\n"
        "⚙️ Хочешь изменить детализацию?\n"
        "Используй `/width 160`\n\n"
        "❓ Подробная инструкция — `/help`"
    )


@dp.message(lambda message: message.photo)
async def photo_handler(message: Message):
    with TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)

        input_path = temp_dir / "input.jpg"
        output_path = temp_dir / "output.png"

        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)
        await bot.download_file(
            file.file_path,
            input_path
        )

        width = user_widths.get(
            message.from_user.id,
            default_width
        )

        ascii_image = convert(
            input_path,
            target_width=width
        )

        output_image = render_ascii_to_image(
            ascii_image
        )

        output_image.save(output_path)

        await message.answer_photo(
            FSInputFile(output_path),
            caption=f"Готово! 🗿 Ширина: {width}"
        )

@dp.message(Command("width"))
async def width_handler(message: Message):
    args = message.text.split()

    if len(args) < 2:
        await message.answer(
            "Укажи ширину.\n"
            "Например: /width 160"
        )
        return

    try:
        width = int(args[1])
    except ValueError:
        await message.answer(
            "Ширина должна быть целым числом."
        )
        return

    if width < min_width or width > max_width:
        await message.answer(
            f"Ширина должна быть от {min_width} до {max_width}."
        )
        return

    user_widths[message.from_user.id] = width

    await message.answer(
        f"Ширина установлена: {width}."
    )

@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "🗿 ASCII-art бот\n\n"
        "Отправь мне любое изображение — я превращу его в ASCII-art.\n\n"

        "⚙️ Ширина изображения\n"
        f"По умолчанию: {default_width} символов.\n\n"

        "Изменить ширину:\n"
        "/width 80\n"
        "/width 120\n"
        "/width 200\n"
        "/width 300\n\n"

        f"📌 Доступный диапазон: {min_width}–{max_width}\n"
        "Чем больше ширина — тем больше деталей и размер результата.\n\n"

        "После изменения ширины просто отправь изображение ещё раз.\n\n"

        "📋 Команды\n"
        "/start — начать работу\n"
        "/help — показать эту справку\n"
        "/width <число> — изменить ширину ASCII-art"
    )

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())