import json
import random
import logging
import os
import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# ТВОЙ ТОКЕН
TOKEN = '8343143228:AAE-KnaSdHOc855mH64LMREQyzxfZ-kptRU'

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_random_challenge():
    """Безопасное чтение случайного условия из JSON."""
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, 'challenges.json')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            challenges = data.get('challenges', [])
            return random.choice(challenges) if challenges else "⚠️ Список пуст!"
    except Exception as e:
        return f"❌ Ошибка файла: {e}"

def get_keyboard():
    """Создание инлайн-клавиатуры через Builder."""
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Испытать удачу! 🎰", 
        callback_data="roll")
    )
    return builder.as_markup()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "⚔️ **Clash Royale Challenge (Aiogram v3)** ⚔️\n\n"
        "Нажми кнопку, чтобы получить случайное условие!",
        reply_markup=get_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

# Обработчик нажатия на кнопку (callback_data="roll")
@dp.callback_query(F.data == "roll")
async def handle_roll(callback: types.CallbackQuery):
    challenge = get_random_challenge()
    icon = random.choice(['🏆', '⭐️', '👑', '🎲', '⚡️'])
    
    # Текст для обновления
    new_text = f"{icon} **ТВОЁ УСЛОВИЕ:**\n\n> {challenge}\n\n_Удачи в испытании!_"
    
    # Редактируем сообщение (с защитой от ошибки, если текст не изменился)
    try:
        await callback.message.edit_text(
            text=new_text,
            reply_markup=get_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception:
        pass
    
    # Убираем "часики" на кнопке
    await callback.answer()

async def main():
    print("--- Бот на AIOGRAM запущен ---")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
