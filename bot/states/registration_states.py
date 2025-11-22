from aiogram.fsm.state import StatesGroup, State

class RegistrationStates(StatesGroup):
    choose_role = State()
    enter_fullname= State()
    choose_region = State()
    enter_city = State()
    choose_category = State()
    get_contact = State()
    registration_user = State()