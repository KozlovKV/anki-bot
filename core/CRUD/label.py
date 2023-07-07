from . import Label, CardLabelRelation
from . import utils


def create(user_id: int, name: str, is_private=False):
    label = Label(
        user_id=user_id, name=name,
        is_private=is_private
    )
    label.save()
    return label


def update(user_id, label_id, name: str, is_private=False):
    label = utils.user_protected_read(Label, user_id, label_id)
    label.name = name
    label.is_private = is_private
    label.save()
    return label


def delete(user_id, label_id):
    label = utils.user_protected_read(Label, user_id, label_id)
    CardLabelRelation.delete().where(CardLabelRelation.label == label).execute()
    return label.delete_instance()
