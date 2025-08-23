from datetime import datetime
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply import lead_type_kb, cancel_kb, skip_kb, back_to_menu_kb
from schemas.lead import LeadCreate
from utils.decorators import require_auth
from services.user_cache import get_leads_cached, get_user_data_cached
from states.states import CreateLeadStates
from services.api_client import create_lead

router = Router()

@router.message(Command("createLead"))
@require_auth(redirect_to_auth=True)
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
        preferred_date = datetime.strptime(message.text, "%d.%m %H:%M").replace(year=datetime.now().year)
    except ValueError:
        await message.answer("Неверный формат времени. Попробуйте ещё раз (например: 25.12 14:30)")
        return
    
    await state.update_data(preferred_date=preferred_date.isoformat())
    await message.answer("Введите дополнительный комментарий / описание проблемы", reply_markup=skip_kb)
    await state.set_state(CreateLeadStates.lead_comment)

@router.message(CreateLeadStates.lead_comment)
async def get_comment(message: Message, state: FSMContext):
    if message.text == "Пропустить":
        comment = ""
    else:
        comment = message.text
    
    data = await state.get_data()
    user_data = await get_user_data_cached(message.from_user.id)

    lead = LeadCreate(
        user_id=user_data.id,
        service_type=data.get("service_type"),
        preferred_date=data.get("preferred_date"),
        comment=comment
    )
    
    if await create_lead(message.from_user.id, lead):
        await message.answer(
            "🎉 **Заявка создана успешно!**\n\n"
            f"🦷 Услуга: {data.get('service_type')}\n\n"
            f"📅 Желаемое время: {data.get('preferred_date')}\n\n"
            f"📝 Комментарий: {comment}\n\n"
            f"📞 Мы свяжемся с вами для уточнения времени и деталей."
            f"Спасибо за обращение!",
            reply_markup=back_to_menu_kb,
            parse_mode="Markdown"
        )
    else:
        await message.answer("Произошла ошибка, заявка не была создана")

    await state.clear()

@router.message(Command("showLeads"))
async def show_leads(message: Message):
    leads = await get_leads_cached(message.from_user.id)

    if not leads:
        await message.answer("У вас нет записей!", reply_markup=back_to_menu_kb)
        return
    
    message_text = "Ваши записи:\n\n"
    for lead in leads:
        preferred_date = datetime.fromisoformat(lead.preferred_date)
        message_text += (
            f"Тип услуги: {lead.service_type}\n"
            f"Желаемое время: {preferred_date.strftime('%d.%m в %H:%M')}\n"
            f"Время записи: {lead.appointment_date if lead.appointment_date else 'Не уточнено'}\n"
            f"Комментарий: {lead.comment}\n\n"
        )

    await message.answer(message_text, reply_markup=back_to_menu_kb)