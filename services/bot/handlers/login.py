from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

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
    
    login_data = {
        "login": data["login"],
        "password": message.text
    }

    responce = await login_user(login_data)

    await message.answer(f"{dict(responce).get('login')}, вход успешно завершен! \n" 
                         f"Ваши данные: {responce}")
    await state.clear()


async def cancel_login(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Вход отменен", reply_markup=auth_kb)