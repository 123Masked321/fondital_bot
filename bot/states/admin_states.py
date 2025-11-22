from aiogram.fsm.state import StatesGroup, State


class SelectSpecStates(StatesGroup):
    choose_category = State()
    get_info = State()


class AddProductStates(StatesGroup):
    processing_data = State()
    processing_brand = State()
    processing_type = State()
    processing_title = State()
    processing_instruction = State()
    processing_access = State()
    processing_document = State()
    processing_adding = State()


class DeleteProductStates(StatesGroup):
    processing_data = State()
    processing_brand = State()
    processing_type = State()
    processing_instruction = State()
    processing_deleting = State()
    processing_confirm = State()


class SendMessages(StatesGroup):
    processing_category = State()
    processing_area = State()
    processing_text = State()