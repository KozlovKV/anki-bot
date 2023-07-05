from . import CardLabelRelation, Card, Label


def create(card, label, is_reversed=False):
    relation = CardLabelRelation(
        card=card, label=label,
        is_reversed=is_reversed
    )
    relation.save()
    return relation


def readOne(label, card):
    return (CardLabelRelation.get_or_none(card=card, label=label)).dict()


def readAllCardsByLabel(label):
    relations = CardLabelRelation.select().join(Card).where(CardLabelRelation.label == label)
    return [relation.card for relation in relations]


def readAllLabelsByCard(card):
    relations = CardLabelRelation.select().join(Label).where(CardLabelRelation.card == card)
    return [relation.label for relation in relations]


def delete(card, label):
    relation = CardLabelRelation.get_or_none(card=card, label=label)
    if not relation:
        raise IndexError
    return relation.delete_instance()
