from typing import Optional

import telebot

from . import keyboards
from . import messages


class ViewPrototype:
    def __init__(
            self, bot: telebot.TeleBot,
            message: Optional[telebot.types.Message] = None,
            call: Optional[telebot.types.CallbackQuery] = None,
            other_instance=None
    ):
        self.bot = bot
        self.temp_storage = {}
        if message:
            self.chat_id = message.chat.id
            self.message_id = message.id
            self.user_id = message.from_user.id
        elif call:
            self.chat_id = call.message.chat.id
            self.message_id = call.message.id
            self.user_id = call.from_user.id
        else:
            self.chat_id = other_instance.chat_id
            self.message_id = other_instance.message_id
            self.user_id = other_instance.user_id


class BaseView(ViewPrototype):
    def send_welcome(self):
        self.bot.send_message(self.chat_id, messages.WELCOME, reply_markup=keyboards.get_base_inline_menu())

    def send_settings_message(self):
        self.bot.send_message(self.chat_id, messages.SETTINGS, reply_markup=keyboards.get_base_inline_menu())

    def send_menu(self):
        self.bot.send_message(self.chat_id, messages.MENU, reply_markup=keyboards.get_base_inline_menu())

    def disable_inline_and_send_menu(self):
        self.bot.edit_message_reply_markup(self.chat_id, self.message_id)
        self.send_menu()

    def edit_to_base_menu(self, message_text=messages.MENU):
        self.bot.edit_message_text(
            message_text, self.chat_id, self.message_id,
            reply_markup=keyboards.get_base_inline_menu()
        )

    def send_info(self):
        self.bot.send_message(self.chat_id, messages.INFO_1, parse_mode='MarkdownV2')
        self.bot.send_message(self.chat_id, messages.INFO_2, parse_mode='MarkdownV2')
        self.bot.send_message(self.chat_id, messages.INFO_3)
        self.send_menu()

    def send_help(self):
        self.bot.send_message(self.chat_id, messages.HELP_1)
        self.bot.send_message(self.chat_id, messages.HELP_2)
        self.send_menu()

    def send_contacts(self):
        self.bot.send_message(self.chat_id, messages.CONTACT)
        self.send_menu()
