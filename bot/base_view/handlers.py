import telebot

from . import keyboards
from . import messages


def bind_handlers(bot: telebot.TeleBot):
    bot.register_message_handler(
        send_welcome, commands=['start'], pass_bot=True
    )
    bot.register_message_handler(
        show_menu, commands=['keyboard'], pass_bot=True
    )
    bot.register_message_handler(
        send_settings_message, commands=['settings'], pass_bot=True
    )
    bot.register_message_handler(
        send_info, commands=['info'], pass_bot=True
    )
    bot.register_message_handler(
        send_help, commands=['help'], pass_bot=True
    )
    bot.register_message_handler(
        send_contacts, commands=['contact'], pass_bot=True
    )


def send_welcome(message: telebot.types.Message, bot: telebot.TeleBot):
    bot.send_message(message.chat.id, messages.WELCOME, reply_markup=keyboards.get_base_markup())


def send_settings_message(message: telebot.types.Message, bot: telebot.TeleBot):
    bot.send_message(message.chat.id, messages.SETTINGS, reply_markup=keyboards.get_base_markup())


def show_menu(message: telebot.types.Message, bot: telebot.TeleBot):
    bot.send_message(message.chat.id, 'Доступные действия', reply_markup=keyboards.get_base_markup())


def send_info(message: telebot.types.Message, bot: telebot.TeleBot):
    bot.send_message(message.chat.id, messages.INFO_1, parse_mode='MarkdownV2')
    bot.send_message(message.chat.id, messages.INFO_2, parse_mode='MarkdownV2')
    bot.send_message(message.chat.id, messages.INFO_3, reply_markup=keyboards.get_base_markup())


def send_help(message: telebot.types.Message, bot: telebot.TeleBot):
    bot.send_message(message.chat.id, messages.HELP_1)
    bot.send_message(message.chat.id, messages.HELP_2, reply_markup=keyboards.get_base_markup())


def send_contacts(message: telebot.types.Message, bot: telebot.TeleBot):
    bot.send_message(message.chat.id, messages.CONTACT, reply_markup=keyboards.get_base_markup())
