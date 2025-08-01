from aiogram.fsm.state import State, StatesGroup

class RegisterStates(StatesGroup):
    register_login = State()
    register_password = State()
    register_full_name = State()
    register_contact_phone = State()

class LoginStates(StatesGroup):
    login_login = State()
    login_password = State()