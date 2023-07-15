from core import anki_engine


from bot.base_view.views import BaseView
from bot.card_view.views import CardView

import bot.base_view.keyboards as base_keyboards
import bot.label_view.keyboards as label_keyboards

from . import keyboards
from . import messages


class RelationView(BaseView):
    def set_label_cards_inline_for_chaining(self, label_id: int):
        label = anki_engine.utils.user_protected_read(
            anki_engine.Label, self.user_id, label_id
        )
        cards = anki_engine.get_user_cards(self.user_id)
        self.bot.edit_message_text(
            messages.CARDS_INLINE_SWITCHING,
            self.chat_id, self.message_id,
            reply_markup=keyboards.get_label_to_cards_switch_inline(label, cards)
        )

    def switch_label_card_relation(self, label_id: int, card_id: int):
        anki_engine.relation_controls.switch_relation(self.user_id, card_id, label_id)
        self.set_label_cards_inline_for_chaining(label_id)

    def set_card_labels_inline_for_chaining(self, card_id: int):
        card = anki_engine.utils.user_protected_read(anki_engine.Card, self.user_id, card_id)
        labels = anki_engine.get_user_labels(self.user_id)
        inline = keyboards.get_card_switch_inline(card_id, labels)
        self.bot.edit_message_text(card.str_with_labels(), self.chat_id, self.message_id, reply_markup=inline)

    def switch_card_label_relation(self, card_id: int, label_id: int):
        anki_engine.relation_controls.switch_relation(self.user_id, card_id, label_id)
        self.set_card_labels_inline_for_chaining(card_id)

    def set_label_copy_relations_inline(self, from_label_id: int):
        labels = anki_engine.get_user_labels(self.user_id)
        self.bot.edit_message_text(
            messages.COPY_RELATIONS_START_MESSAGE, self.chat_id, self.message_id,
            reply_markup=keyboards.get_label_copy_inline(from_label_id, labels)
        )

    def copy_relations(self, from_label_id: int, to_label_id: int):
        anki_engine.relation_controls.copy_relation_from_other_label(self.user_id, to_label_id, from_label_id)
        to_label = anki_engine.utils.user_protected_read(anki_engine.Label, self.user_id, to_label_id)
        from_label = anki_engine.utils.user_protected_read(anki_engine.Label, self.user_id, from_label_id)
        self.bot.edit_message_text(
            messages.get_copy_relations_success(from_label.name, to_label.name),
            self.chat_id, self.message_id,
            reply_markup=base_keyboards.get_base_inline_menu()
        )