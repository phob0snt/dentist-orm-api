from aiogram.fsm.state import State, StatesGroup

class RegisterStates(StatesGroup):
    waiting_for_login = State()
    waiting_for_password = State()
    waiting_for_full_name = State()
    waiting_for_contact_phone = State()