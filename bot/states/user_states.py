from aiogram.fsm.state import StatesGroup, State


class Boiler(StatesGroup):
    choose_brand = State()
    choose_category = State()
    choose_error = State()
    choose_detail_error = State()
    choose_model = State()
    choose_instruction = State()
    choose_detail_instruction = State()


class ChangeFullname(StatesGroup):
    change_database = State()


class ChangeCity(StatesGroup):
    enter_city = State()
    change_database = State()