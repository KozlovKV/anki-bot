from . import CardLabelRelation, Card, Label
from . import utils


def create(user_id, card_id, label_id, is_reversed=False):
    card = utils.user_protected_read(Card, user_id, card_id)
    label = utils.user_protected_read(Label, user_id, label_id)
    return CardLabelRelation.get_or_create(
        card=card, label=label,
        is_reversed=is_reversed
    )


def read_one(user_id, label_id, card_id):
    return create(user_id, card_id, label_id)


def delete(user_id, card_id, label_id):
    card = utils.user_protected_read(Card, user_id, card_id)
    label = utils.user_protected_read(Label, user_id, label_id)
    relation = CardLabelRelation.get_or_none(card=card, label=label)
    if not relation:
        raise IndexError
    return relation.delete_instance()
