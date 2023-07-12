from . import CardLabelRelation, Card, Label
from . import utils


def create(user_id, card_id, label_id, is_reversed=False) -> [CardLabelRelation, bool]:
    card = utils.user_protected_read(Card, user_id, card_id)
    label = utils.user_protected_read(Label, user_id, label_id)
    return CardLabelRelation.get_or_create(
        card=card, label=label,
        is_reversed=is_reversed
    )


def create_by_instances(card: Card, label: Label, is_reversed=False) -> [CardLabelRelation, bool]:
    return CardLabelRelation.get_or_create(
        card=card, label=label,
        is_reversed=is_reversed
    )


def read_one(user_id, label_id, card_id) -> [CardLabelRelation, bool]:
    return create(user_id, card_id, label_id)


def switch_relation(user_id, card_id, label_id) -> [CardLabelRelation, bool]:
    relation_with_flag = create(user_id, card_id, label_id)
    if relation_with_flag[1]:
        return relation_with_flag[0]
    relation_with_flag[0].delete_instance()
    return None


def copy_relation_from_other_label(user_id: int, target_label_id: int, source_label_id: int):
    target_label: Label = utils.user_protected_read(Label, user_id, target_label_id)
    source_label: Label = utils.user_protected_read(Label, user_id, source_label_id)
    source_label_cards = source_label.get_cards()
    for card in source_label_cards:
        create_by_instances(card, target_label)


def delete(user_id, card_id, label_id):
    card = utils.user_protected_read(Card, user_id, card_id)
    label = utils.user_protected_read(Label, user_id, label_id)
    relation = CardLabelRelation.get_or_none(card=card, label=label)
    if not relation:
        raise IndexError
    return relation.delete_instance()
