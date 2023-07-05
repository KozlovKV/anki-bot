from datetime import datetime
from . import MemNote, Card
from . import DEFAULT_DAYS_BEFORE_REPEATING_FIRST
from . import DEFAULT_DAYS_BEFORE_REPEATING_SECOND
from . import DEFAULT_EASINESS_FACTOR


def memNote2Dict(mem_note) -> dict:
    if not mem_note:
        return None
    return {
        'last_repeating': mem_note.last_repeating,
        'days_before_repeating': mem_note.days_before_repeating,
        'easiness_factor': mem_note.easiness_factor
    }


def create(card: Card, user_id: int):
    note = MemNote(
        user_id=user_id, card=card,
        last_repeating=datetime.now()
    )
    note.save()
    return note


def readOne(card, user_id):
    return memNote2Dict(MemNote.get_or_none(card=card, user_id=user_id))


RESET_LIMIT = 3
MAX_QUALITY = 5


def recalculate_memory_note(note, quality):
    note.last_repeating = datetime.now()

    if quality > MAX_QUALITY:
        quality = MAX_QUALITY

    note.easiness_factor = note.easiness_factor + (
            0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    )
    if note.easiness_factor < 1.3:
        note.easiness_factor = 1.3

    if quality < RESET_LIMIT:
        note.days_before_repeating = DEFAULT_DAYS_BEFORE_REPEATING_FIRST
    elif note.days_before_repeating == 1:
        note.days_before_repeating = DEFAULT_DAYS_BEFORE_REPEATING_SECOND
    else:
        note.days_before_repeating = round(note.days_before_repeating * note.easiness_factor)

    note.save()
    return note


def delete(card, user_id):
    note = MemNote.get_or_none(card=card, user_id=user_id)
    if not note:
        return None
    return note.delete_instance()
