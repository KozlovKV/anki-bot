import telebot

from core import anki_engine

from bot.base_view.views import ViewPrototype

from . import keyboards
from . import messages


class CardView(ViewPrototype):
    def ask_first_card_side(self):
        self.edit_to_cancel_message()
        placeholder = telebot.types.ForceReply(input_field_placeholder=messages.FIRST_SIDE_PLACEHOLDER)
        return self.send_temp_message(messages.FIRST_SIDE_MESSAGE, reply_markup=placeholder)

    def ask_second_card_side(self):
        self.add_temp_message_id(self.message_id)
        placeholder = telebot.types.ForceReply(input_field_placeholder=messages.SECOND_SIDE_PLACEHOLDER)
        return self.send_temp_message(messages.SECOND_SIDE_MESSAGE, reply_markup=placeholder)

    def create_card(self, side1: str, side2: str):
        self.add_temp_message_id(self.message_id)
        card = anki_engine.card_controls.create(self.user_id, side1, side2)
        self.delete_temp_messages()
        self.send_card(card)

    def send_card(
            self, card: anki_engine.Card,
            markup_function=keyboards.get_base_card_inline
    ):
        self.update_current_menu(
            self.bot.send_message(
                self.chat_id, card.str_with_labels(),
                reply_markup=markup_function(card.id)
            ).id
        )

    def set_card_with_base_inline(self, card_id: int):
        self.delete_temp_messages()
        card = anki_engine.utils.user_protected_read(anki_engine.Card, self.user_id, card_id)
        self.bot.edit_message_text(
            card.str_with_labels(),
            self.chat_id, self.message_id,
            reply_markup=keyboards.get_base_card_inline(card.id)
        )

    def set_user_cards_inline(self):
        cards = anki_engine.get_user_cards(self.user_id)
        if len(cards) == 0:
            self.edit_to_base_menu(messages.EMPTY_CARDS_LIST)
            return
        inline = keyboards.get_cards_choose_inline(cards)
        self.bot.edit_message_text(
            messages.CARDS_CHOOSING,
            self.chat_id, self.message_id,
            reply_markup=inline
        )

    def set_edit_side_inline(self, card_id: int):
        self.bot.edit_message_reply_markup(
            self.chat_id, self.message_id,
            reply_markup=keyboards.get_edit_card_inline(card_id)
        )

    def ask_new_side_text(self, card_id: int, side_number: int):
        self.bot.edit_message_reply_markup(
            self.chat_id, self.message_id, reply_markup=keyboards.get_card_back_inline(card_id)
        )
        message_dict = messages.get_edit_side_message_dict(side_number)
        placeholder = telebot.types.ForceReply(
            input_field_placeholder=message_dict['placeholder']
        )
        return self.send_temp_message(
            message_dict['message'], reply_markup=placeholder
        )

    def edit_side(self, card_id: int, side_number: int, side_text: str):
        self.add_temp_message_id(self.message_id)
        card = anki_engine.utils.user_protected_read(anki_engine.Card, self.user_id, card_id)
        if side_number == 1:
            card.side1 = side_text
        else:
            card.side2 = side_text
        card.save()
        self.delete_temp_messages()
        self.send_card(card)

    def ask_deletion_proof(self, card_id: int):
        self.bot.edit_message_reply_markup(
            self.chat_id, self.message_id,
            reply_markup=keyboards.get_delete_card_inline(card_id)
        )

    def delete_card(self, card_id):
        anki_engine.card_controls.delete(self.user_id, card_id)
        self.edit_to_base_menu(messages.DELETE_CARD_SUCCESS)


