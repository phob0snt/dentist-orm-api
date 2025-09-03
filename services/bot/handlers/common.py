from aiogram import Bot, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply import auth_kb, menu_kb
from schemas.auth import UserData
from services.auth_rpc import refresh_token_pair
from utils.jwt import validate_token
from services.user_cache import get_user_data_cached, get_leads_cached
from redis_utils.tokens import get_token
from utils.decorators import require_auth

from .lead import show_leads, start_lead_creation
from .register import start_registration
from .login import start_login


router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id

    access_token = await get_token("access_token", user_id)
    if access_token:
        if validate_token(access_token):
            await show_main_page(message)
            return
    refresh_token = await get_token("refresh_token", user_id)
    if refresh_token:
        if await refresh_token_pair(user_id, refresh_token):
            await show_main_page(message)
            return
    
    await message.answer("Добро пожаловать в Dentist!\n" \
    "Зарегистрируйтесь или войдите в свой аккаунт для доступа к услугам нашей стоматологии",
    reply_markup=auth_kb)

@router.message(Command("auth"))
async def show_auth_menu(message: Message, error_message: str = None):
    if error_message:
        text = f"{error_message}\n\n"
    text += (
        "Для использования бота необходимо войти в систему.\n\n"
        "• 🔐 **Войти** - если у вас уже есть аккаунт\n"
        "• 📝 **Регистрация** - создать новый аккаунт\n"
    )
    await message.answer(text, reply_markup=auth_kb)

@router.message(Command("main"))
@require_auth(redirect_to_auth=True)
async def show_main_page(message: Message):
    user_data: UserData = await get_user_data_cached(message.from_user.id, True)
    leads = await get_leads_cached(message.from_user.id, True)
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
@require_auth(redirect_to_auth=True)
async def create_lead_button_handler(message: Message, state: FSMContext):
    await start_lead_creation(message, state)

@router.message(lambda m: m.text == "Мои записи")
@require_auth(redirect_to_auth=True)
async def show_leads_button_handler(message: Message):
    await show_leads(message)

@router.message(lambda m: m.text == "На главную")
@require_auth(redirect_to_auth=True)
async def create_lead_button_handler(message: Message):
    await show_main_page(message)