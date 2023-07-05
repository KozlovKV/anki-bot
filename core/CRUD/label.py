from . import Label


def label2Dict(label) -> dict:
    if not label:
        return None
    return {
        'id': label.id,
        'user_id': label.user_id,
        'name': label.name,
        'side1Name': label.side1Name,
        'side2Name': label.side2Name,
        'is_private': label.is_private
    }


def create(user_id: int, name: str, side1: str, side2: str, is_private=False):
    label = Label(
        user_id=user_id, name=name,
        side1Name=side1, side2Name=side2,
        is_private=is_private
    )
    label.save()
    return label


def readOne(label_id):
    return label2Dict(Label.get_or_none(id=label_id))


def readAllUserCards(user_id):
    labels = Label.select().where(Label.user_id == user_id)
    return [label2Dict(label) for label in labels]


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
