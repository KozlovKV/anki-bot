import telebot
import datetime

from . import keyboards
from . import messages


def bind_handlers(bot: telebot.TeleBot):
    # bot.register_message_handler(
    #     base_log, func=lambda _: True
    # )
    bot.register_callback_query_handler(
        edit_to_base_menu,
        func=lambda call: keyboards.BaseMenuUrls.BASE_MENU in call.data,
        pass_bot=True
    )
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
    bot.send_message(message.chat.id, messages.WELCOME, reply_markup=keyboards.get_base_inline_menu())


def send_settings_message(message: telebot.types.Message, bot: telebot.TeleBot):
    bot.send_message(message.chat.id, messages.SETTINGS, reply_markup=keyboards.get_base_inline_menu())


def show_menu(message: telebot.types.Message, bot: telebot.TeleBot):
    bot.send_message(message.chat.id, messages.MENU, reply_markup=keyboards.get_base_inline_menu())


def edit_to_base_menu(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    bot.edit_message_text(
        messages.MENU, call.message.chat.id, call.message.id,
        reply_markup=keyboards.get_base_inline_menu()
    )


def send_info(message: telebot.types.Message, bot: telebot.TeleBot):
    bot.send_message(message.chat.id, messages.INFO_1, parse_mode='MarkdownV2')
    bot.send_message(message.chat.id, messages.INFO_2, parse_mode='MarkdownV2')
    bot.send_message(message.chat.id, messages.INFO_3)
    show_menu(message, bot)


def send_help(message: telebot.types.Message, bot: telebot.TeleBot):
    bot.send_message(message.chat.id, messages.HELP_1)
    bot.send_message(message.chat.id, messages.HELP_2)
    show_menu(message, bot)


def send_contacts(message: telebot.types.Message, bot: telebot.TeleBot):
    bot.send_message(message.chat.id, messages.CONTACT)
    show_menu(message, bot)


def base_log(message: telebot.types.Message):
    print(f'{datetime.datetime.now()}: user {message.from_user.id} in chat {message.chat.id} '
          f'sent {message.text} with type {message.content_type}')
