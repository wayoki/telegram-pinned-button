import asyncio
from pathlib import Path
from aiogram import Bot
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "" # токен, получаемый при регистрации бота в BotFather
CHANNEL_ID = "@channel_id" # канал в котором бот выложит пост
URL = "https://t.me/wayoki" # вводите любой url на который будет переадресация по кнопке
BUTTON_TEXT = "BUTTON TEXT" # текст внутри самой кнопки
TEXT = """
TEXT
""".strip()  # текст поста

PHOTO = {".jpg", ".jpeg", ".png", ".webp"} # форматы, которые поддерживаются для фото
VIDEO = {".mp4", ".mov", ".avi", ".mkv"} # для видео

def get_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=BUTTON_TEXT, url=URL)]
        ]
    )

def get_media_file():
    files = [
        file for file in Path(".").iterdir()
        if file.is_file() and file.suffix.lower() in PHOTO | VIDEO
    ]
    if len(files) > 1:
        return "Выберите только 1 файл!"

    return files[0] if files else None

async def send_post(bot, media_file):
    keyboard = get_keyboard()
    if media_file is None:
        return await bot.send_message(
            chat_id=CHANNEL_ID,
            text=TEXT,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    file = FSInputFile(media_file)
    ext = media_file.suffix.lower()
    if ext in PHOTO:
        return await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=file,
            caption=TEXT,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    return await bot.send_video(
        chat_id=CHANNEL_ID,
        video=file,
        caption=TEXT,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

async def main():
    media_file = get_media_file()
    if media_file == "Выберите только 1 файл!":
        print("Выберите только 1 файл!")
        return
    bot = Bot(token=BOT_TOKEN)
    message = await send_post(bot, media_file)
    await bot.pin_chat_message(
        chat_id=CHANNEL_ID,
        message_id=message.message_id,
        disable_notification=True
    )
    await bot.session.close()

asyncio.run(main())
