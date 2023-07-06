from . import Label, CardLabelRelation


def create(user_id: int, name: str, is_private=False):
    label = Label(
        user_id=user_id, name=name,
        is_private=is_private
    )
    label.save()
    return label


def update(user_id, label_id, name: str, is_private=False):
    label = Label.get_or_none(id=label_id)
    if not label:
        raise IndexError
    if int(label.user_id) != user_id:
        raise PermissionError
    label.name = name
    label.is_private = is_private
    label.save()
    return label


def delete(user_id, label_id):
    label = Label.get_or_none(id=label_id)
    if not label:
        raise IndexError
    if int(label.user_id) != user_id:
        raise PermissionError
    CardLabelRelation.delete().where(CardLabelRelation.label == labels_list[label_index]).execute()
    return label.delete_instance()
