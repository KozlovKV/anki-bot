from datetime import timedelta, datetime
from typing import List

from .models import Card, Label, CardLabelRelation, MemNote
from .models import DEFAULT_DAYS_BEFORE_REPEATING_FIRST
from .models import DEFAULT_DAYS_BEFORE_REPEATING_SECOND

from .CRUD import card as card_controls
from .CRUD import label as label_controls
from .CRUD import cardLabelRelation as relation_controls
from .CRUD import utils


def get_user_cards(user_id: int) -> List[Card]:
    card_select = Card.select().where(Card.user_id == user_id)
    return list(card_select)


def get_user_labels(user_id: int) -> List[Label]:
    labels_select = Label.select().where(Label.user_id == user_id)
    return list(labels_select)


def get_full_card_info_str(card_id):
    return Card.get_by_id(card_id).str_with_labels()


def get_cards_to_train(user_id, label_id, count=10):
    label = utils.empty_protected_read(Label, label_id)
    if label.is_blocked_for_user(user_id):
        raise PermissionError
    cards = label.get_cards()
    trainable_cards = []
    for card in cards:
        if count <= 0:
            break
        if card.can_be_trained(user_id):
            trainable_cards.append(card)
            count -= 1
    return trainable_cards


RESET_LIMIT = 3
MAX_QUALITY = 5


def recalculate_memory_note(user_id, card_id, quality):
    card = utils.empty_protected_read(Card, card_id)
    note = card.get_mem_note(user_id)
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
