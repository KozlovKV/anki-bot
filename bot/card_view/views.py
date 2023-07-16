from core import anki_engine

from bot import utils

from bot.base_view.views import BaseView

from . import keyboards
from . import messages


class CardView(BaseView):
    def ask_first_card_side(self):
        self.edit_to_cancel_message()
        new_message = utils.send_message_with_force_reply_placeholder(
            self.bot, self.chat_id, messages.FIRST_SIDE_PLACEHOLDER,
            messages.FIRST_SIDE_MESSAGE
        )
        self.add_temp_message_id(new_message.id)
        return new_message

    def ask_second_card_side(self):
        self.add_temp_message_id(self.message_id)
        new_message = utils.send_message_with_force_reply_placeholder(
            self.bot, self.chat_id, messages.SECOND_SIDE_PLACEHOLDER,
            messages.SECOND_SIDE_MESSAGE
        )
        self.add_temp_message_id(new_message.id)
        return new_message

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
        card = anki_engine.utils.user_protected_read(anki_engine.Card, self.user_id, card_id)
        self.bot.edit_message_text(
            card.str_with_labels(),
            self.chat_id, self.message_id,
            reply_markup=keyboards.get_base_card_inline(card.id)
        )

    def send_user_cards(self, markup_function=keyboards.get_base_card_inline):
        cards = anki_engine.get_user_cards(self.user_id)
        for card in cards:
            self.send_card(card, markup_function)
        if len(cards) == 0:
            self.bot.send_message(self.chat_id, messages.EMPTY_CARDS_LIST)

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

    def ask_new_side_text(self, side_number: int):
        self.edit_to_cancel_message()
        return utils.send_message_with_force_reply_placeholder(
            self.bot, self.chat_id, messages.get_edit_side_placeholder(side_number),
            messages.get_edit_side_message(side_number)
        )

    def edit_side(self, card_id: int, side_number: int, side_text: str):
        card = anki_engine.utils.user_protected_read(anki_engine.Card, self.user_id, card_id)
        if side_number == 1:
            card.side1 = side_text
        else:
            card.side2 = side_text
        card.save()
        self.send_card(card)

    def ask_deletion_proof(self, card_id: int):
        self.bot.edit_message_reply_markup(
            self.chat_id, self.message_id,
            reply_markup=keyboards.get_delete_card_inline(card_id)
        )

    def delete_card(self, card_id):
        anki_engine.card_controls.delete(self.user_id, card_id)
        self.edit_to_base_menu(messages.DELETE_CARD_SUCCESS)


