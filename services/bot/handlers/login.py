from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from schemas.auth import LoginRequest
from states.states import LoginStates
from keyboards.reply import cancel_kb, auth_kb
from services.api_client import login_user


router = Router()

@router.message(Command("login"))
async def start_login(message: Message, state: FSMContext):
    await message.answer("Введите логин:", reply_markup=cancel_kb)
    await state.set_state(LoginStates.login_login)

@router.message(LoginStates.login_login)
async def get_login(message: Message, state: FSMContext):
    if message.text == "Отменить":
        await cancel_login(message, state)
        return
    
    await state.update_data(login=message.text)
    await message.answer("Введите пароль:", reply_markup=cancel_kb)
    await state.set_state(LoginStates.login_password)

@router.message(LoginStates.login_password)
async def get_password(message: Message, state: FSMContext):
    if message.text == "Отменить":
        await cancel_login(message, state)
        return
    
    data = await state.get_data()
    
    login_data = LoginRequest(
        telegram_id=message.from_user.id,
        login = data["login"],
        password =  message.text
    )

    responce = await login_user(login_data)
    if responce:
        from .common import show_main_page
        await show_main_page(message)
    else:
        await message.answer("❌ Не удалось авторизоваться. Попробуйте заново", reply_markup=auth_kb)
    await state.clear()


async def cancel_login(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Вход отменен", reply_markup=auth_kb)