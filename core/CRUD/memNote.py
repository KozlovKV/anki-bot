from datetime import datetime
from . import MemNote, Card


def memNote2Dict(mem_note) -> dict:
    if not mem_note:
        return None
    return {
        'remembering_moment': mem_note.remembering_moment,
        'memorization_level': mem_note.memorization_level,
    }


def create(card: Card, user_id: int):
    note = MemNote(
        user_id=user_id, card=card,
        remembering_moment=datetime.now()
    )
    note.save()
    return note


def readOne(card, user_id):
    return memNote2Dict(MemNote.get_or_none(card=card, user_id=user_id))


MIN_LEVEL = 0
MAX_LEVEL = 10


def change_memorization_level(note, delta):
    note.remembering_moment = datetime.now()
    note.memorization_level += delta
    if note.memorization_level < MIN_LEVEL:
        note.memorization_level = MIN_LEVEL
    elif note.memorization_level > MAX_LEVEL:
        note.memorization_level = MAX_LEVEL
    note.save()
    return note


def delete(card, user_id):
    note = MemNote.get_or_none(card=card, user_id=user_id)
    if not note:
        return None
    return note.delete_instance()
