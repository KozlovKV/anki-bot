from . import CardLabelRelation, Card, Label
from .card import card2Dict
from .label import label2Dict


def cardLabelRelation2Dict(card_label_relation) -> dict:
    if not card_label_relation:
        return None
    return {
        'card': card2Dict(card_label_relation.card),
        'label': label2Dict(card_label_relation.label),
        'is_reversed': card_label_relation.is_reversed
    }


def create(card, label, is_reversed=False):
    relation = CardLabelRelation(
        card=card, label=label,
        is_reversed=is_reversed
    )
    relation.save()
    return relation


def readOne(label, card):
    return cardLabelRelation2Dict(
        CardLabelRelation.get_or_none(card=card, label=label)
    )


def readAllCardsByLabel(label):
    relations = CardLabelRelation.select().join(Card).where(CardLabelRelation.label == label)
    return [card2Dict(relation.card) for relation in relations]


def readAllLabelsByCard(card):
    relations = CardLabelRelation.select().join(Label).where(CardLabelRelation.card == card)
    return [label2Dict(relation.label) for relation in relations]


def delete(card, label):
    relation = CardLabelRelation.get_or_none(card=card, label=label)
    if not relation:
        raise IndexError
    return relation.delete_instance()
