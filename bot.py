from aiogram import Bot, Dispatcher, executor, types
import logging, random, requests

API_TOKEN = "8261801832:AAEHUDbVv1lnBCjHtao_oeGNT_ODowA6Q8g"
SERVER_URL = "https://gockline-serves.onrender.com"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🔐 Получить код")
    await msg.answer("Добро пожаловать в GockLine", reply_markup=kb)

@dp.message_handler(lambda m: m.text == "🔐 Получить код")
async def get_code(msg: types.Message):
    payload = {
        "tg_id": msg.from_user.id,
        "username": msg.from_user.username or f"user{msg.from_user.id}"
    }

    r = requests.post(f"{SERVER_URL}/register", json=payload)

    if r.status_code != 200:
        await msg.answer("❌ Ошибка сервера")
        return

    data = r.json()

    await msg.answer(
        f"✅ Регистрация успешна\n\n"
        f"🆔 ID: {data['id']}\n"
        f"🔑 TOKEN:\n`{data['token']}`\n\n"
        "⚠️ Сохрани токен",
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
