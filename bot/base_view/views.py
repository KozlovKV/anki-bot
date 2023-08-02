from typing import Optional

import telebot

from core.models import DB

from . import keyboards
from . import messages
from . import state


class ViewPrototype:
    def __init__(
            self, bot: telebot.TeleBot,
            message: Optional[telebot.types.Message] = None,
            call: Optional[telebot.types.CallbackQuery] = None,
            other_instance=None
    ):
        DB.connect(True)
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

    def __del__(self):
        DB.close()

    def init_states(self, first_menu_id):
        self.bot.set_state(self.user_id, state.BaseState.current_menu_id)
        self.bot.set_state(self.user_id, state.BaseState.temp_list)
        with self.bot.retrieve_data(self.user_id) as data:
            data['current_menu_id'] = first_menu_id
            data['temp_list'] = []

    def update_current_menu(self, new_menu_id):
        with self.bot.retrieve_data(self.user_id) as data:
            if data['current_menu_id'] != new_menu_id:
                self.bot.delete_message(self.chat_id, data['current_menu_id'])
                data['current_menu_id'] = new_menu_id

    def add_temp_message_id(self, message_id):
        with self.bot.retrieve_data(self.user_id) as data:
            data['temp_list'].append(message_id)

    def delete_temp_messages(self):
        with self.bot.retrieve_data(self.user_id) as data:
            for message_id in data['temp_list']:
                self.bot.delete_message(self.chat_id, message_id)
            data['temp_list'] = []

    def send_menu(self, message_text=messages.MENU):
        self.delete_temp_messages()
        new_menu = self.bot.send_message(
            self.chat_id, message_text,
            reply_markup=keyboards.get_base_inline_menu()
        )
        self.update_current_menu(new_menu.id)
        return new_menu

    def edit_to_base_menu(self, message_text=messages.MENU):
        self.delete_temp_messages()
        edited_menu = self.bot.edit_message_text(
            message_text, self.chat_id, self.message_id,
            reply_markup=keyboards.get_base_inline_menu()
        )
        self.update_current_menu(edited_menu.id)
        return edited_menu

    def send_cancel_message(self, message_text=messages.CANCEL):
        cancel_message = self.bot.send_message(
            self.chat_id, message_text,
            reply_markup=keyboards.get_send_menu_inline()
        )
        self.update_current_menu(cancel_message.id)
        return cancel_message

    def edit_to_cancel_message(self, message_text=messages.CANCEL):
        return self.bot.edit_message_text(
            message_text, self.chat_id, self.message_id,
            reply_markup=keyboards.get_send_menu_inline()
        )

    def send_temp_message(self, message_text, **kwargs):
        message = self.bot.send_message(self.chat_id, message_text, **kwargs)
        self.add_temp_message_id(message.id)
        return message


class BaseView(ViewPrototype):
    def send_welcome(self):
        self.init_states(
            self.bot.send_message(
                self.chat_id, messages.WELCOME,
                reply_markup=keyboards.get_base_inline_menu()
            ).id
        )

    def send_keyboard_from_command(self):
        self.add_temp_message_id(self.message_id)
        self.send_menu(messages.SETTINGS)

    def send_settings_message(self):
        self.add_temp_message_id(self.message_id)
        self.send_menu(messages.SETTINGS)

    def send_info(self):
        self.add_temp_message_id(self.message_id)
        self.send_temp_message(messages.INFO_1, parse_mode='MarkdownV2')
        self.send_temp_message(messages.INFO_2, parse_mode='MarkdownV2')
        self.send_temp_message(messages.INFO_3)
        self.send_cancel_message(messages.RETURN)

    def send_help(self):
        self.add_temp_message_id(self.message_id)
        self.send_temp_message(messages.HELP_1)
        self.send_temp_message(messages.HELP_2)
        self.send_cancel_message(messages.RETURN)

    def send_contacts(self):
        self.add_temp_message_id(self.message_id)
        self.send_temp_message(messages.CONTACT)
        self.send_cancel_message(messages.RETURN)
