# bot.py
import os, asyncio
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")   # <-- KALIT NOMI
WEBAPP_URL = os.getenv("WEBAPP_URL")

def mask(v): return "None" if not v else f"{v[:8]}...{v[-6:]}"

print(f"[env] .env -> {BASE_DIR / '.env'} exists={(BASE_DIR / '.env').exists()}")
print(f"[env] TELEGRAM_BOT_TOKEN loaded? {bool(BOT_TOKEN)} value={mask(BOT_TOKEN)}")
print(f"[env] WEBAPP_URL={WEBAPP_URL}")

if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN topilmadi. .env yoki export ni tekshir.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(m: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🍬 Candy Shop’ni ochish",
                             web_app=WebAppInfo(url=WEBAPP_URL))
    ]])
    await m.answer("Candy Shop’ga xush kelibsiz!", reply_markup=kb)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
