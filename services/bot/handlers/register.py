from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.states import RegisterStates


router = Router()

@router.message(F.text == "/register")
async def start_registration(message: Message, state: FSMContext):
    await message.answer("Как вас зовут?")
    await state.set_state(RegisterStates.waiting_for_full_name)

@router.message(RegisterStates.waiting_for_full_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Укажите телефон для уточнения времени записи")
    await state.set_state(RegisterStates.waiting_for_contact_phone)

@router.message(RegisterStates.waiting_for_contact_phone)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(contact_phone=message.text)
    await message.answer("Придумайте логин для доступа в личный кабинет")
    await state.set_state(RegisterStates.waiting_for_login)

@router.message(RegisterStates.waiting_for_login)
async def get_login(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Придумайте пароль")
    await state.set_state(RegisterStates.waiting_for_password)

@router.message(RegisterStates.waiting_for_password)
async def get_password(message: Message, state: FSMContext):
    data = await state.get_data()
    full_name = data["name"]
    contact_phone = data["contact_phone"]
    login = data["login"]
    password = message.text

    await message.answer(f"{full_name}, регистрация успешно завершена!")
    await state.clear()