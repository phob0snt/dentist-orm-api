from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply import auth_kb, menu_kb
from schemas.auth import UserData
from services.user_cache import get_user_data_cached, get_leads_cached

from .lead import show_leads, start_lead_creation
from .register import start_registration
from .login import start_login


router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Добро пожаловать в Dentist!" \
    "Зарегистрируйтесь или войдите в свой аккаунт для доступа к услугам нашей стоматологии",
    reply_markup=auth_kb)

@router.message(Command("main"))
async def show_main_page(message: Message):
    user_data: UserData = await get_user_data_cached(message.from_user.id)
    leads = await get_leads_cached(message.from_user.id)
    leads_count = len(leads) if leads else 0

    await message.answer(
        f"Добро пожаловать, {user_data.full_name}! \n"
        f"Ваши записи: {leads_count}",
        reply_markup=menu_kb
    )

@router.message(lambda m: m.text == "📝 Регистрация")
async def registration_button_handler(message: Message, state: FSMContext):
    await start_registration(message, state)

@router.message(lambda m: m.text == "🔐 Войти")
async def login_button_handler(message: Message, state: FSMContext):
    await start_login(message, state)

@router.message(lambda m: m.text == "Записаться на прием")
async def create_lead_button_handler(message: Message, state: FSMContext):
    await start_lead_creation(message, state)

@router.message(lambda m: m.text == "Мои записи")
async def show_leads_button_handler(message: Message):
    await show_leads(message)

@router.message(lambda m: m.text == "На главную")
async def create_lead_button_handler(message: Message):
    await show_main_page(message)