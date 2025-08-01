from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.main import main_kb
from .register import start_registration
from .login import start_login


router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Добро пожаловать в Dentist!" \
    "Зарегистрируйтесь или войдите в свой аккаунт для доступа к услугам нашей стоматологии",
    reply_markup=main_kb)

@router.message(lambda m: m.text == "📝 Регистрация")
async def registration_button_handler(message: Message, state: FSMContext):
    await start_registration(message, state)

@router.message(lambda m: m.text == "🔐 Войти")
async def login_button_handler(message: Message, state: FSMContext):
    await start_login(message, state)