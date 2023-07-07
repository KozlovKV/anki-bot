from .models import Card, Label, CardLabelRelation, MemNote
from .CRUD import card
from .CRUD import label
from .CRUD import cardLabelRelation
from .CRUD import utils


RESET_LIMIT = 3
MAX_QUALITY = 5


def get_user_cards(user_id: int) -> [Card]:
    card_select = Card.select().where(Card.user_id == user_id)
    return list(card_select)


def get_user_labels(user_id: int) -> [Label]:
    labels_select = Label.select().where(Label.user_id == user_id)
    return list(labels_select)


def get_full_card_info_str(card_id):
    return Card.get_by_id(card_id).str_with_labels()


# def get_cards_to_train(user_id, label_id, count=10):
#     label = Label.get_by_id(label_id)
#     if label.is_private and int(label.user_id) != user_id:
#         raise PermissionError
#     cards = label.get_cards()
#     trainable_cards = []
#     for card in cards:
#         if count <= 0:
#             break
#         note = card.get_mem_note(user_id)
#         days_delta = timedelta(note.days_before_repeating-1)
#         if datetime.now() - note.last_repeating > days_delta:
#             trainable_cards.append((card, note))
#             count -= 1
#     return trainable_cards
#
#
# def recalculate_memory_note(user_id, card_id, quality):
#     note = trainable_cards[train_card_index][1]
#     note.last_repeating = datetime.now()
#
#     if quality > MAX_QUALITY:
#         quality = MAX_QUALITY
#
#     note.easiness_factor = note.easiness_factor + (
#             0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
#     )
#     if note.easiness_factor < 1.3:
#         note.easiness_factor = 1.3
#
#     if quality < RESET_LIMIT:
#         note.days_before_repeating = DEFAULT_DAYS_BEFORE_REPEATING_FIRST
#     elif note.days_before_repeating == DEFAULT_DAYS_BEFORE_REPEATING_FIRST:
#         note.days_before_repeating = DEFAULT_DAYS_BEFORE_REPEATING_SECOND
#     else:
#         note.days_before_repeating = round(note.days_before_repeating * note.easiness_factor)
#
#     note.save()
#     return note
