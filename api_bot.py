import asyncio
import random
import requests
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from deep_translator import GoogleTranslator

from config import TOKEN, THE_CAT_API_KEY, NASA_API_KEY, NEWS_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()



def get_random_cat():
    url = "https://api.thecatapi.com/v1/images/search"
    headers = {"x-api-key": THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data[0]['url']


def get_random_apod():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    random_date = start_date + (end_date - start_date) * random.random()
    date_str = random_date.strftime("%Y-%m-%d")

    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}"
    response = requests.get(url)
    return response.json()


def get_random_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=10&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    articles = data.get("articles", [])
    if not articles:
        return None

    article = random.choice(articles)

    return {
        "title": article["title"],
        "description": article["description"],
        "url": article["url"],
        "image": article["urlToImage"]
    }


def translate_to_ru(text: str) -> str:
    try:
        translator = GoogleTranslator(source='en', target='ru')
        return translator.translate(text)
    except Exception as e:
        print("Translation error:", e)
        return text


def get_random_quote():
    try:
        url = "https://zenquotes.io/api/random"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            print("ZenQuotes error:", response.status_code)
            return "Ошибка получения цитаты."

        data = response.json()

        quote_en = data[0]["q"]
        author = data[0]["a"]

        quote_ru = translate_to_ru(quote_en)

        return f"{quote_ru}\n\n— {author}"

    except Exception as e:
        print("Quote error:", e)
        return "Ошибка получения цитаты."


@dp.message(Command("start"))
async def start(message: Message):
    text = (
        "Привет 👋\n\n"
        "Доступные команды:\n"
        "/cat — случайный кот 🐱\n"
        "/space — случайное космическое фото 🚀\n"
        "/news — случайная новость 📰\n"
        "/quote — случайная цитата 💬"
    )
    await message.answer(text)


@dp.message(Command("cat"))
async def send_cat(message: Message):
    photo = get_random_cat()
    await message.answer_photo(photo=photo)


@dp.message(Command("space"))
async def send_space(message: Message):
    apod = get_random_apod()

    if apod.get("media_type") != "image":
        await message.answer("Сегодня не изображение, попробуйте ещё раз.")
        return

    await message.answer_photo(
        photo=apod["url"],
        caption=f"{apod['title']}\n\n{apod['explanation'][:500]}..."
    )


@dp.message(Command("news"))
async def send_news(message: Message):
    news = get_random_news()

    if not news:
        await message.answer("Не удалось получить новости.")
        return

    caption = (
        f"📰 {news['title']}\n\n"
        f"{news['description']}\n\n"
        f"Читать полностью: {news['url']}"
    )

    if news["image"]:
        await message.answer_photo(photo=news["image"], caption=caption)
    else:
        await message.answer(caption)


@dp.message(Command("quote"))
async def send_quote(message: Message):
    quote = get_random_quote()
    await message.answer(quote)



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
