from aiogram.fsm.state import State, StatesGroup

class RegisterStates(StatesGroup):
    register_login = State()
    register_password = State()
    register_full_name = State()
    register_contact_phone = State()

class LoginStates(StatesGroup):
    login_login = State()
    login_password = State()

class CreateLeadStates(StatesGroup):
    lead_service_type = State()
    lead_preferred_date = State()
    lead_comment = State()