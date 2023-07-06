from . import Card, CardLabelRelation, MemNote


def create(user_id: int, side1: str, side2: str):
    card = Card(user_id=user_id, side1=side1, side2=side2)
    card.save()
    return card


def update(user_id, card_id, side1: str, side2: str):
    card = Card.get_or_none(id=card_id)
    if not card:
        raise IndexError
    if int(card.user_id) != user_id:
        raise PermissionError
    card.side1 = side1
    card.side2 = side2
    card.save()
    return card


def delete(user_id, card_id):
    card = Card.get_or_none(id=card_id)
    if not card:
        raise IndexError
    if int(card.user_id) != user_id:
        raise PermissionError
    CardLabelRelation.delete().where(CardLabelRelation.card == card).execute()
    MemNote.delete().where(MemNote.card == card).execute()
    return card.delete_instance()
