from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

auth_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Регистрация")],
        [KeyboardButton(text="🔐 Войти")]
    ],
    resize_keyboard=True
)

cancel_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отменить")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Записаться на прием")],
        [KeyboardButton(text="Мои записи")]
    ],
    resize_keyboard=True
)

lead_type_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Гигиена")],
        [KeyboardButton(text="Лечение")],
        [KeyboardButton(text="Протезирование")],
        [KeyboardButton(text="Другое")]
    ],
    resize_keyboard=True
)

skip_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Пропустить")]
    ],
    resize_keyboard=True
)