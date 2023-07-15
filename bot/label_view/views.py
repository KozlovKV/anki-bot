from core import anki_engine

from bot import utils

from bot.base_view.views import BaseView

from . import keyboards
from . import messages


class LabelView(BaseView):
    def ask_private_flag(self):
        self.bot.edit_message_text(
            messages.IS_PUBLIC_MESSAGE, self.chat_id, self.message_id,
            reply_markup=keyboards.get_yes_no_inline()
        )

    def ask_label_name(self, is_private: bool):
        self.edit_to_cancel_message()
        message_dict = messages.get_label_name_message_dict(is_private)
        return utils.send_message_with_force_reply_placeholder(
            self.bot, self.chat_id, message_dict['placeholder'],
            message_dict['message']
        )

    def create_label(self, is_private: bool, label_name: str):
        label = anki_engine.label_controls.create(self.user_id, label_name, is_private)
        self.send_label(label)

    def show_user_labels(self):
        self.bot.edit_message_text(
            messages.CHOOSE_LABEL,
            self.chat_id, self.message_id,
            reply_markup=keyboards.get_labels_as_inline(
                anki_engine.get_user_labels(self.user_id)
            )
        )

    def set_base_label_inline(self, label_id: int):
        label = anki_engine.utils.empty_protected_read(anki_engine.Label, label_id)
        self.bot.edit_message_text(
            label.full_str, self.chat_id, self.message_id,
            reply_markup=keyboards.get_base_label_inline(label_id)
        )

    def send_label(self, label: anki_engine.Label, markup_function=keyboards.get_base_label_inline):
        return self.bot.send_message(
            self.chat_id, label.full_str,
            reply_markup=markup_function(label.id)
        )

    def set_edit_label_inline(self, label_id: int):
        self.bot.edit_message_reply_markup(
            self.chat_id, self.message_id,
            reply_markup=keyboards.get_edit_label_inline(label_id)
        )

    def switch_label_permission(self, label_id: int):
        label = anki_engine.label_controls.switch_permission(self.user_id, label_id)
        self.bot.edit_message_text(
            label.full_str, self.chat_id, self.message_id,
            reply_markup=keyboards.get_base_label_inline(label_id)
        )

    def ask_new_label_name(self):
        self.edit_to_cancel_message()
        return utils.send_message_with_force_reply_placeholder(
            self.bot, self.chat_id, messages.EDIT_LABEL_NAME_PLACEHOLDER,
            messages.EDIT_LABEL_NAME_MESSAGE
        )

    def edit_label_name(self, label_id, new_label_name: str):
        label = anki_engine.label_controls.update(self.user_id, label_id, new_label_name)
        label.save()
        self.send_label(label)

    def ask_label_deletion_proof(self, label_id: int):
        self.bot.edit_message_reply_markup(
            self.chat_id, self.message_id,
            reply_markup=keyboards.get_delete_label_inline(label_id)
        )

    def delete_label(self, label_id: int):
        anki_engine.label_controls.delete(self.user_id, label_id)
        self.edit_to_base_menu(messages.LABEL_DELETED)
