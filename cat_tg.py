import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
import requests

from config import TOKEN, THE_CAT_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_cat_breeds():
    url = 'https://api.thecatapi.com/v1/breeds'
    headers = {"x-api-key":THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def get_cat_image_by_breed(breed_id):
    url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
    headers = {"x-api-key": THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data[0]['url']

def get_breed_info(breed_name):
   breeds = get_cat_breeds()
   for breed in breeds:
       if breed['name'].lower() == breed_name.lower():
           return breed
   return None

@dp.message(Command("start"))
async def start_command(message: Message):
   await message.answer("Привет! Напиши мне название породы кошки, и я пришлю тебе её фото и описание.")


@dp.message(Command("breeds"))
async def breeds_command(message: Message):
    breeds = get_cat_breeds()
    # Сортируем породы по алфавиту
    sorted_breeds = sorted(breeds, key=lambda x: x['name'])

    # Создаем список пород с указанием, что они кликабельные
    breeds_list = []
    for breed in sorted_breeds:
        breeds_list.append(f"▪️ {breed['name']}")

    # Разбиваем на части, если список слишком длинный
    all_breeds = "\n".join(breeds_list)

    if len(all_breeds) > 4096:
        chunks = []
        current_chunk = ""
        for breed_line in breeds_list:
            if len(current_chunk) + len(breed_line) + 1 < 4096:
                current_chunk += breed_line + "\n"
            else:
                chunks.append(current_chunk)
                current_chunk = breed_line + "\n"
        chunks.append(current_chunk)

        await message.answer("📋 Список доступных пород (часть 1). Нажмите на название, чтобы выбрать:")
        for i, chunk in enumerate(chunks, 1):
            await message.answer(chunk)
    else:
        await message.answer(f"📋 Список доступных пород. Нажмите на название, чтобы выбрать:\n\n{all_breeds}")

@dp.message()
async def send_cat_info(message: Message):
   breed_name = message.text
   breed_info = get_breed_info(breed_name)
   if breed_info:
       cat_image_url = get_cat_image_by_breed(breed_info['id'])
       info = (
           f"Порода - {breed_info['name']}\\n"
           f"Описание - {breed_info['description']}\\n"
           f"Продолжительность жизни - {breed_info['life_span']} лет"
       )
       await message.answer_photo(photo=cat_image_url, caption=info)
   else:
       await message.answer("Порода не найдена. Попробуйте еще раз.")


async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())