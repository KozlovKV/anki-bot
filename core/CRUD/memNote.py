from datetime import datetime
from . import MemNote, Card



def create(card: Card, user_id: int):
    note = MemNote(
        user_id=user_id, card=card,
        last_repeating=datetime.now()
    )
    note.save()
    return note


def readOne(card, user_id):
    return MemNote.get_or_create(card=card, user_id=user_id, defaults={'last_repeating': datetime.now()})[0]


def delete(card, user_id):
    note = MemNote.get_or_none(card=card, user_id=user_id)
    if not note:
        return None
    return note.delete_instance()
