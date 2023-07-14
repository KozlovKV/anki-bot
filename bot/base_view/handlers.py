import telebot

from .views import BaseView
from . import keyboards


def bind_handlers(bot: telebot.TeleBot):
    bot.register_callback_query_handler(
        handle_base_menu_query,
        func=lambda call: keyboards.BaseMenuUrls.BASE_MENU in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_base_menu_query,
        func=lambda call: keyboards.BaseMenuUrls.BASE_MENU_NEW in call.data,
        pass_bot=True
    )
    bot.register_message_handler(
        handle_start_command, commands=['start'], pass_bot=True
    )
    bot.register_message_handler(
        handle_keyboard_command, commands=['keyboard'], pass_bot=True
    )
    bot.register_message_handler(
        handle_settings_command, commands=['settings'], pass_bot=True
    )
    bot.register_message_handler(
        handle_info_command, commands=['info'], pass_bot=True
    )
    bot.register_message_handler(
        handle_help_command, commands=['help'], pass_bot=True
    )
    bot.register_message_handler(
        handle_contacts_command, commands=['contact'], pass_bot=True
    )


def handle_start_command(message: telebot.types.Message, bot: telebot.TeleBot):
    BaseView(bot, message=message).send_welcome()


def handle_settings_command(message: telebot.types.Message, bot: telebot.TeleBot):
    BaseView(bot, message=message).send_settings_message()


def handle_keyboard_command(message: telebot.types.Message, bot: telebot.TeleBot):
    BaseView(bot, message=message).send_menu()


def handle_base_menu_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    BaseView(bot, call=call).edit_to_base_menu()


def handle_info_command(message: telebot.types.Message, bot: telebot.TeleBot):
    BaseView(bot, message=message).send_info()


def handle_help_command(message: telebot.types.Message, bot: telebot.TeleBot):
    BaseView(bot, message=message).send_help()


def handle_contacts_command(message: telebot.types.Message, bot: telebot.TeleBot):
    BaseView(bot, message=message).send_contacts()
