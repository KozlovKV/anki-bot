from datetime import datetime, timedelta

from .models import DEFAULT_DAYS_BEFORE_REPEATING_FIRST
from .models import DEFAULT_DAYS_BEFORE_REPEATING_SECOND
from .models import DEFAULT_EASINESS_FACTOR

from .models import Card, Label, CardLabelRelation, MemNote
from .CRUD import label as label_crud, cardLabelRelation as CLR_crud, memNote as memNote_crud


RESET_LIMIT = 3
MAX_QUALITY = 5


class AnkiSession:
    """
    Main class for session with DB for Anki training.

    Fields with postfix 'select' represent the SQL queries and can be outdated at some time.
    Fields with postfix 'list' represent actual data for current user
    """
    def __init__(self, user_id):
        self.user_id = user_id
        self.labels_select = None
        self.labels_list = []
        self.cards_select = None
        self.cards_list = []
        self.trainable_cards = []

        self.get_user_labels()
        self.get_user_cards()

    def get_user_cards(self):
        self.cards_select = Card.select().where(Card.user_id == self.user_id)
        self.cards_list = list(self.cards_select)
        return self.cards_select

    def get_user_labels(self):
        self.labels_select = Label.select().where(Label.user_id == self.user_id)
        self.labels_list = list(self.labels_select)
        return self.labels_select

    def get_full_card_info_str(self, card_index):
        return self.cards_list[card_index].str_with_labels()

    def get_cards_to_train(self, label, count=10):
        if label.is_private and int(label.user_id) != self.user_id:
            raise PermissionError
        cards = label.get_cards()
        self.trainable_cards = []
        for card in cards:
            if count <= 0:
                break
            note = memNote_crud.readOne(card, self.user_id)
            days_delta = timedelta(note.days_before_repeating-1)
            if datetime.now() - note.last_repeating > days_delta:
                self.trainable_cards.append((card, note))
                count -= 1
        return self.trainable_cards

    def recalculate_memory_note(self, train_card_index, quality):
        note = self.trainable_cards[train_card_index][1]
        note.last_repeating = datetime.now()

        if quality > MAX_QUALITY:
            quality = MAX_QUALITY

        note.easiness_factor = note.easiness_factor + (
                0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
        )
        if note.easiness_factor < 1.3:
            note.easiness_factor = 1.3

        if quality < RESET_LIMIT:
            note.days_before_repeating = DEFAULT_DAYS_BEFORE_REPEATING_FIRST
        elif note.days_before_repeating == DEFAULT_DAYS_BEFORE_REPEATING_FIRST:
            note.days_before_repeating = DEFAULT_DAYS_BEFORE_REPEATING_SECOND
        else:
            note.days_before_repeating = round(note.days_before_repeating * note.easiness_factor)

        note.save()
        return note

    def create_card(self, string: str):
        """Create card from format '<side1> / <side2>'"""
        sides = list(map(lambda s: s.strip(), string.split('/')))
        card = Card(user_id=self.user_id, side1=sides[0], side2=sides[1])
        card.save()
        self.cards_list.append(card)
        return card

    def update_card(self, card_index, string: str):
        """Update card from format '<side1> / <side2>'"""
        sides = list(map(lambda s: s.strip(), string.split('/')))
        self.cards_list[card_index].side1 = sides[0]
        self.cards_list[card_index].side2 = sides[1]
        self.cards_list[card_index].save()

    def create_label(self, string: str, is_private: bool):
        """Create label from format '<name>'"""
        label = Label(
            user_id=self.user_id, name=string.strip(),
            is_private=is_private
        )
        label.save()
        self.labels_list.append(label)
        return label

    def update_label(self, label_index, string: str, is_private: bool):
        """Create label from format '<name>'"""
        self.labels_list[label_index].name = string.strip()
        self.labels_list[label_index].is_private = is_private
        self.labels_list[label_index].save()

    def create_relation(self, card_index, label_index):
        return CardLabelRelation.get_or_create(card=self.cards_list[card_index], label=self.labels_list[label_index])

    def delete_card(self, card_index):
        CardLabelRelation.delete().where(CardLabelRelation.card == self.cards_list[card_index]).execute()
        MemNote.delete().where(MemNote.card == self.cards_list[card_index]).execute()
        self.cards_list[card_index].delete_instance()
        self.cards_list.pop(card_index)

    def delete_label(self, label_index):
        CardLabelRelation.delete().where(CardLabelRelation.label == self.labels_list[label_index]).execute()
        self.labels_list[label_index].delete_instance()
        self.labels_list.pop(label_index)


