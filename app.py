import asyncio
import os
from threading import Thread
from flask import Flask
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ========== ВСТАВЬТЕ СВОЙ ТОКЕН ==========
TOKEN = "8853216028:AAEoArmQI4Gyo-QiM-ZD2yuux_dJ-d18ZaM"

# ========== ВАШИ ССЫЛКИ НА КАНАЛЫ ==========
LINKS = {
    "✨ Общий гороскоп на сегодня ✨": "https://t.me/YourAstro12",
    "Овен": "https://t.me/aries12121212",
    "Телец": "https://t.me/Taurus12121212",
    "Близнецы": "https://t.me/gemini12121212",
    "Рак": "https://t.me/cancer12121212",
    "Лев": "https://t.me/LEO121212121",
    "Дева": "https://t.me/virgo1212121",
    "Весы": "https://t.me/Libra12121",
    "Скорпион": "https://t.me/scorpi12121",
    "Стрелец": "https://t.me/Sagittarius12121",
    "Козерог": "https://t.me/+Pa_pHFcaaVg3MzEy",
    "Водолей": "https://t.me/+TvlMA37fFxpmNzcy",
    "Рыбы": "https://t.me/+6DDnaRvP_KM0NTYy"
}

# ========== НАСТРОЙКА БОТА ==========
bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_main_keyboard():
    buttons = []
    signs = list(LINKS.keys())
    for i in range(0, len(signs), 3):
        row = signs[i:i+3]
        buttons.append([InlineKeyboardButton(text=sign, callback_data=sign) for sign in row])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "✨ *Добро пожаловать в навигатор по знакам зодиака!* ✨\n\n"
        "Выберите свой знак, чтобы перейти в канал с гороскопами и астрологией.\n"
        "Или загляните в общий канал с гороскопом на сегодня для всех знаков! 🌟",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    sign = callback.data
    link = LINKS.get(sign)
    if link:
        await callback.message.answer(
            f"🔮 *{sign}*\n\n"
            f"Вот ссылка на канал:\n{link}\n\n"
            "Нажмите на неё и подпишитесь!",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
    else:
        await callback.message.answer("❌ Ссылка не найдена.")
    await callback.answer()

# ========== ВЕБ-СЕРВЕР ДЛЯ RENDER ==========
# Это заставляет Render думать, что приложение постоянно работает
app = Flask(__name__)

@app.route('/')
def home():
    return "✨ Бот-навигатор по знакам зодиака работает! ✨"

@app.route('/health')
def health():
    return "OK", 200

def run_bot():
    """Запускает Telegram-бота в отдельном потоке"""
    asyncio.run(dp.start_polling(bot))

# Запускаем бота в фоновом потоке
if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    
    # Запускаем Flask-сервер (он занимает порт для Render)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)