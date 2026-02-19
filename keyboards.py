from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ---------- Задание 1: Reply-кнопки "Привет" / "Пока" ----------
# Создаём клавиатуру с двумя кнопками в один ряд.
# resize_keyboard=True делает кнопки маленькими и компактными.
reply_hello_bye = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")]
    ],
    resize_keyboard=True
)

# ---------- Задание 2: Inline-кнопки со ссылками ----------
# Простая инлайн-клавиатура со ссылками. Каждая кнопка — отдельный ряд.
inline_links = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Новости", url="https://ria.ru")],
        [InlineKeyboardButton(text="Музыка", url="https://music.yandex.ru")],
        [InlineKeyboardButton(text="Видео", url="https://youtube.com")]
    ]
)

# ---------- Задание 3: Динамическая клавиатура (с builder) ----------
async def dynamic_keyboard(show_more: bool = True):
    """
    Если show_more=True — показываем кнопку "Показать больше".
    Если False — показываем кнопки "Опция 1" и "Опция 2".
    """
    keyboard = InlineKeyboardBuilder()

    if show_more:
        # Первый шаг: только одна кнопка "Показать больше"
        keyboard.add(InlineKeyboardButton(
            text="Показать больше ➕",
            callback_data="show_more"
        ))
    else:
        # Второй шаг: две опции
        keyboard.add(
            InlineKeyboardButton(text="Опция 1", callback_data="opt_1"),
            InlineKeyboardButton(text="Опция 2", callback_data="opt_2")
        )
        # Размещаем по одной кнопке в ряд (можно убрать, если хочешь в ряд)
        keyboard.adjust(2)  # 2 кнопки в одном ряду

    return keyboard.as_markup()