import telebot

from core import anki_engine

from bot import utils

from bot.base_view.views import ViewPrototype
from bot.label_view.views import LabelView

import bot.base_view.keyboards as base_keyboards

from . import keyboards
from . import messages
from . import state


class TrainView(ViewPrototype):
    def ask_label_id_first_with_canceling_option(self):
        self.edit_to_cancel_message()
        return self.ask_label_id()

    def ask_label_id(self):
        placeholder = telebot.types.ForceReply(input_field_placeholder=messages.ASK_LABEL_ID_PLACEHOLDER)
        return self.send_temp_message(messages.ASK_LABEL_ID_MESSAGE, reply_markup=placeholder)

    def send_nan_message(self, next_message_function, *args):
        self.add_temp_message_id(self.message_id)
        self.send_temp_message(
            messages.NAN_ERROR_MESSAGE, reply_to_message_id=self.message_id
        )
        return next_message_function(*args)

    def get_label_from_reply(self, label_id: int):
        self.add_temp_message_id(self.message_id)
        try:
            label = anki_engine.utils.empty_protected_read(anki_engine.Label, label_id)
            self.temp_storage['label_id'] = label_id
        except IndexError:
            self.send_menu(messages.NOT_EXIST_LABEL_ID_MESSAGE)
            return None
        if label.is_blocked_for_user(self.user_id):
            self.send_menu(messages.BLOCKED_LABEL_MESSAGE)
            return None
        self.delete_temp_messages()
        LabelView(self.bot, other_instance=self).send_label(
            label, lambda _: base_keyboards.get_back_menu_inline('Отмена тренировки')
        )
        return self.ask_count()

    def ask_count_with_canceling_option(self, label_id: int):
        label = anki_engine.utils.empty_protected_read(anki_engine.Label, label_id)
        self.edit_to_cancel_message(
            messages.get_label_received_message(label.name)
        )
        return self.ask_count()

    def ask_count(self):
        placeholder = telebot.types.ForceReply(input_field_placeholder=messages.ASK_COUNT_PLACEHOLDER)
        return self.send_temp_message(messages.ASK_COUNT_MESSAGE, reply_markup=placeholder)

    def start_train(self, label_id, count):
        self.add_temp_message_id(self.message_id)
        train_list = anki_engine.get_cards_to_train(self.user_id, label_id, count)
        length = len(train_list)
        if length == 0:
            self.send_menu(messages.EMPTY_TRAIN_LIST)
        else:
            self.bot.set_state(self.user_id, state.TrainState.train_list)
            self.bot.set_state(self.user_id, state.TrainState.train_list_length)
            with self.bot.retrieve_data(self.user_id) as data:
                data['train_list'] = train_list
                data['train_list_length'] = length
            self.send_next_trainable_card()

    def send_next_trainable_card(self):
        with self.bot.retrieve_data(self.user_id) as data:
            card = data['train_list'][0]
            self.send_temp_message(
                messages.get_trainable_card_new_message(data['train_list_length'], str(card.side1)),
                reply_markup=keyboards.get_show_second_side_markup(card.id),
            )

    def edit_to_next_trainable_card(self):
        with self.bot.retrieve_data(self.user_id) as data:
            card = data['train_list'][0]
            self.bot.edit_message_text(
                messages.get_trainable_card_new_message(data['train_list_length'], str(card.side1)),
                self.chat_id, self.message_id,
                reply_markup=keyboards.get_show_second_side_markup(card.id)
            )

    def show_second_side(self):
        with self.bot.retrieve_data(self.user_id) as data:
            card = data['train_list'][0]
            self.bot.edit_message_text(
                messages.get_trainable_card_main_message(data['train_list_length'], str(card)),
                self.chat_id, self.message_id,
                reply_markup=keyboards.get_quality_markup(card.id)
            )

    def recalculate_card(self, card_id, quality):
        anki_engine.recalculate_memory_note(self.user_id, card_id, quality)
        with self.bot.retrieve_data(self.user_id) as data:
            data['train_list'] = data['train_list'][1:]
            data['train_list_length'] -= 1
            length = data['train_list_length']
        if length > 0:
            self.edit_to_next_trainable_card()
        else:
            self.bot.delete_message(
                self.chat_id, self.message_id
            )
            self.send_menu(messages.TRAIN_ENDS)
