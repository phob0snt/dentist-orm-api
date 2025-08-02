from datetime import datetime
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply import lead_type_kb, cancel_kb, skip_kb
from schemas.lead import LeadCreate
from states.states import CreateLeadStates
from services.api_client import create_lead

router = Router()

@router.message(lambda m: m.text == "Записаться на прием")
async def create_lead_button_handler(message: Message, state: FSMContext):
    await start_lead_creation(message, state)

@router.message(Command("createLead"))
async def start_lead_creation(message: Message, state: FSMContext):
    await message.answer("Выберите услугу", reply_markup=lead_type_kb, parse_mode="Markdown")
    await state.set_state(CreateLeadStates.lead_service_type)

@router.message(CreateLeadStates.lead_service_type, F.text.in_(
    ["Гигиена", "Лечение", "Протезирование", "Другое"]
))
async def service_type_selected(message: Message, state: FSMContext):
    await state.update_data(service_type=message.text)
    await message.answer(f"✅ Выбрана услуга: **{message.text}**")
    await message.answer(
        "Введите желаемое время записи, например: '25.12 14:30'",
        reply_markup=cancel_kb
    )
    await state.set_state(CreateLeadStates.lead_preferred_date)

@router.message(CreateLeadStates.lead_preferred_date)
async def get_preferred_date(message: Message, state: FSMContext):
    try:
        preferred_date = datetime.strptime(message.text, "%d.%m %H:%M")
    except ValueError:
        await message.answer("Неверный формат времени. Попробуйте ещё раз (например: 25.12 14:30)")
        return
    
    await state.update_data(preferred_date=preferred_date)
    await message.answer("Введите дополнительный комментарий / описание проблемы", reply_markup=skip_kb)
    await state.set_state(CreateLeadStates.lead_comment)

@router.message(CreateLeadStates.lead_comment)
async def get_comment(message: Message, state: FSMContext):
    if message.text == "Пропустить":
        comment = ""
    else:
        comment = message.text
    
    data = await state.get_data()

    lead = LeadCreate(
        service_type=data.get("service_type"),
        preferred_date=data.get("preferred_date"),
        comment=comment
    )
    
    if await create_lead(lead):
        await message.answer("Заявка успешно создана")
    else:
        await message.answer("Произошла ошибка, заявка не была создана")