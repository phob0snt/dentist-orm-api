from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from schemas.auth import RegisterRequest
from states.states import RegisterStates
from services.bot.keyboards.reply import cancel_kb, auth_kb
from services.api_client import register_user


router = Router()

@router.message(Command("register"))
async def start_registration(message: Message, state: FSMContext):
    await message.answer("Как вас зовут?", reply_markup=cancel_kb)
    await state.set_state(RegisterStates.register_full_name)

@router.message(RegisterStates.register_full_name)
async def get_name(message: Message, state: FSMContext):
    if message.text == "Отменить":
        await cancel_registration(message, state)
        return
    
    await state.update_data(name=message.text)
    await message.answer("Укажите телефон для уточнения времени записи", reply_markup=cancel_kb)
    await state.set_state(RegisterStates.register_contact_phone)

@router.message(RegisterStates.register_contact_phone)
async def get_phone(message: Message, state: FSMContext):
    if message.text == "Отменить":
        await cancel_registration(message, state)
        return
    
    await state.update_data(contact_phone=message.text)
    await message.answer("Придумайте логин для доступа в личный кабинет", reply_markup=cancel_kb)
    await state.set_state(RegisterStates.register_login)

@router.message(RegisterStates.register_login)
async def get_login(message: Message, state: FSMContext):
    if message.text == "Отменить":
        await cancel_registration(message, state)
        return
    
    await state.update_data(login=message.text)
    await message.answer("Придумайте пароль", reply_markup=cancel_kb)
    await state.set_state(RegisterStates.register_password)

@router.message(RegisterStates.register_password)
async def get_password(message: Message, state: FSMContext):
    if message.text == "Отменить":
        await cancel_registration(message, state)
        return
    
    data = await state.get_data()
    
    register_data = RegisterRequest(
        full_name=data["name"],
        contact_phone=data["contact_phone"],
        login=data["login"],
        password=message.text,
        telegram_id=str(message.from_user.id)
    )

    responce = await register_user(register_data)

    await message.answer(f"{data['name']}, регистрация успешно завершена! \n" 
                         f"Ваши данные: {responce}")
    await state.clear()

async def cancel_registration(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Регистрация отменена", reply_markup=auth_kb)