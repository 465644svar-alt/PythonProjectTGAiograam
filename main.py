import asyncio
import requests
import dp
import aiohttp

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN, WEATHER_API_KEY
import random

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Константы для погоды
# WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
DEFAULT_CITY = "Moscow"  # Можете заменить на свой город


# 4. ДОБАВЛЕНО - функция погоды
async def get_weather():
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": DEFAULT_CITY,
        "lang": "ru"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                return f"❌ Ошибка API: {response.status}"

            data = await response.json()

            temp = data["current"]["temp_c"]
            condition = data["current"]["condition"]["text"]

            return f"🌡 {DEFAULT_CITY}: {temp}°C\n☁️ {condition}"

@dp.message(Command('weather'))
async def weather_command(message: Message):
    await message.answer("⏳ Получаю погоду...")
    result = await get_weather()
    await message.answer(result)

@dp.message(Command('test'))
async def test_command(message: Message):
    """Тестовая команда для проверки API"""
    await message.answer("🔍 Проверяю API ключ...")

    # Проверяем, есть ли ключ
    if not WEATHER_API_KEY:
        await message.answer("❌ API ключ не найден в config.py!")
        return

    # Пробуем сделать простой запрос
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q=Moscow&lang=ru"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            await message.answer(f"✅ API работает! Город: {data['location']['name']}, {data['location']['country']}")
        else:
            await message.answer(f"❌ Ошибка API: {response.status_code}\n{response.text}")
    except Exception as e:
        await message.answer(f"❌ Ошибка соединения: {e}")

@dp.message(Command('photo'))
async def photo(message:Message):
    list = ['https://img.freepik.com/premium-vector/colorful-car-with-rainbow-colors-side_1288234-5172.jpg?semt=ais_hybrid',
            'https://img.freepik.com/premium-photo/high-quality-digital-art-wallpaper_783884-246180.jpg?semt=ais_hybrid&w=740',
            'https://img.freepik.com/premium-photo/luxurious-long-hair-kitten-with-bright-blue-eyes-abstract-glowing-neon-light_1113121-3993.jpg?semt=ais_hybrid&w=740']
    rand_photo= random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')


@dp.message(F.photo)
async def react_photo(message:Message):
    list = [ 'Огогошеньки какая фотка!', 'Ух тыыыы', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)


@dp.message(F.text == "Что такое ИИ?")
async def aitext(message:Message):
    await message.answer('Искусственный интеллект (ИИ) — это направление науки, которое занимается разработкой компьютерных систем, способных выполнять задачи, свойственные человеческому интеллекту. Сюда входит анализ данных, распознавание образов, обработка текстов и запросов, сформулированных естественным языком, обучение на потоках данных и принятие решений.')

@dp.message(Command('help'))
async def help(message:Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start \n /help \n /photo \n /weather')

@dp.message(CommandStart())
async def start(message:Message):
    await message.answer("Приветики! Я - Бот!")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())