from datetime import datetime, timedelta

from .models import DEFAULT_DAYS_BEFORE_REPEATING_FIRST
from .models import DEFAULT_DAYS_BEFORE_REPEATING_SECOND
from .models import DEFAULT_EASINESS_FACTOR

from .models import Card, Label, CardLabelRelation, MemNote
from .CRUD import label as label_crud, cardLabelRelation as CLR_crud, memNote as memNote_crud


RESET_LIMIT = 3
MAX_QUALITY = 5


class AnkiSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.labels = Label.select().where(Label.user_id == user_id)
        self.cards = Card.select().where(Card.user_id == user_id)
        self.trainable_cards = []

    def update_cards(self):
        self.cards = Card.select().where(Card.user_id == self.user_id)

    def update_labels(self):
        self.labels = Label.select().where(Label.user_id == self.user_id)

    def get_cards_to_train(self, label, count=10):
        relations = CardLabelRelation.select() \
            .join(Card) \
            .where(
                CardLabelRelation.label == label
            )
        self.trainable_cards = []
        for relation in relations:
            if count <= 0:
                break
            note = memNote_crud.readOne(relation.card, self.user_id)
            days_delta = timedelta(note.days_before_repeating-1)
            if datetime.now() - note.last_repeating > days_delta:
                self.trainable_cards.append((relation.card, note))
                count -= 1
        return self.trainable_cards

    def recalculate_memory_note(self, card_index, quality):
        note = self.trainable_cards[card_index][1]
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
        Card.create(user_id=self.user_id, side1=sides[0], side2=sides[1])


