import telebot


class BaseState(telebot.handler_backends.StatesGroup):
    current_menu_id = telebot.handler_backends.State()
    temp_list = telebot.handler_backends.State()