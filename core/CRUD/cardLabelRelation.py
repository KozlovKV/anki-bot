from . import CardLabelRelation, Card, Label


def create(card, label, is_reversed=False):
    relation = CardLabelRelation(
        card=card, label=label,
        is_reversed=is_reversed
    )
    relation.save()
    return relation


def read_one(label, card):
    return (CardLabelRelation.get_or_none(card=card, label=label)).dict()


def delete(card, label):
    relation = CardLabelRelation.get_or_none(card=card, label=label)
    if not relation:
        raise IndexError
    return relation.delete_instance()
