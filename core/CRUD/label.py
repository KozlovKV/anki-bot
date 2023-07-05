from . import Label


def create(user_id: int, name: str, side1: str, side2: str, is_private=False):
    label = Label(
        user_id=user_id, name=name,
        side1Name=side1, side2Name=side2,
        is_private=is_private
    )
    label.save()
    return label


def readAllUserLabels(user_id):
    labels = Label.select().where(Label.user_id == user_id)
    return [label.dict() for label in labels]


def update(user_id, label_id, name: str, side1: str, side2: str, is_private=False):
    label = Label.get_or_none(id=label_id)
    if not label:
        raise IndexError
    if int(label.user_id) != user_id:
        raise PermissionError
    label.name = name
    label.side1Name = side1
    label.side2Name = side2
    label.is_private = is_private
    label.save()
    return label


def delete(user_id, label_id):
    label = Label.get_or_none(id=label_id)
    if not label:
        raise IndexError
    if int(label.user_id) != user_id:
        raise PermissionError
    return label.delete_instance()
