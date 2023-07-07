from . import Card, CardLabelRelation, MemNote
from . import utils


def create(user_id: int, side1: str, side2: str):
    card = Card(user_id=user_id, side1=side1, side2=side2)
    card.save()
    return card


def update(user_id, card_id, side1: str, side2: str):
    card = utils.user_protected_read(Card, user_id, card_id)
    card.side1 = side1
    card.side2 = side2
    card.save()
    return card


def delete(user_id, card_id):
    card = utils.user_protected_read(Card, user_id, card_id)
    CardLabelRelation.delete().where(CardLabelRelation.card == card).execute()
    MemNote.delete().where(MemNote.card == card).execute()
    return card.delete_instance()
