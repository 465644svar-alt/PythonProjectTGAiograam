import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from config import TOKEN
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ---------- Задание 1: Обработка /start и reply-кнопок ----------
@dp.message(CommandStart())
async def cmd_start(message: Message):
    """Отправляем приветствие и показываем Reply-клавиатуру."""
    await message.answer(
        f"Привет, {message.from_user.first_name}! Выбери действие:",
        reply_markup=kb.reply_hello_bye
    )

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📋 Список доступных команд:\n"
        "/start - начать работу\n"
        "/help - показать это сообщение\n"
        "/links - полезные ссылки\n"
        "/dynamic - динамическое меню\n"
        "/info - информация о пользователе"
    )

@dp.message(Command("info"))
async def cmd_info(message: Message):
    user = message.from_user
    await message.answer(
        f"📊 Информация о пользователе:\n"
        f"ID: {user.id}\n"
        f"Имя: {user.first_name}\n"
        f"Фамилия: {user.last_name or 'не указана'}\n"
        f"Username: @{user.username or 'нет'}"
    )

# Обработка нажатия на Reply-кнопку "Привет"
@dp.message(F.text == "Привет")
async def reply_hello(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

# Обработка нажатия на Reply-кнопку "Пока"
@dp.message(F.text == "Пока")
async def reply_bye(message: Message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")

# ---------- Задание 2: Команда /links ----------
@dp.message(Command("links"))
async def cmd_links(message: Message):
    """Показываем инлайн-кнопки со ссылками."""
    await message.answer(
        "Полезные ссылки:",
        reply_markup=kb.inline_links
    )

# ---------- Задание 3: Команда /dynamic и обработка колбэков ----------
@dp.message(Command("dynamic"))
async def cmd_dynamic(message: Message):
    """Первый экран динамической клавиатуры (кнопка 'Показать больше')."""
    await message.answer(
        "Динамическое меню:",
        reply_markup=await kb.dynamic_keyboard(show_more=True)
    )

# Обработка нажатия на "Показать больше"
@dp.callback_query(F.data == "show_more")
async def process_show_more(callback: CallbackQuery):
    """Заменяем сообщение на новое с кнопками 'Опция 1' и 'Опция 2'."""
    await callback.answer("Загружаем опции...")  # короткое уведомление
    await callback.message.edit_text(
        "Выбери опцию:",
        reply_markup=await kb.dynamic_keyboard(show_more=False)
    )

# Обработка нажатия на "Опция 1"
@dp.callback_query(F.data == "opt_1")
async def process_opt_1(callback: CallbackQuery):
    await callback.answer()  # просто закрываем "часики"
    await callback.message.answer("Ты выбрал Опцию 1 ✅")

# Обработка нажатия на "Опция 2"
@dp.callback_query(F.data == "opt_2")
async def process_opt_2(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Ты выбрал Опцию 2 ✅")

# ---------- Запуск бота ----------
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())