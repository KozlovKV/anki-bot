from datetime import timedelta, datetime
from peewee import *
import sys

from . import config

if '--sqlite' in sys.argv:
    DB = SqliteDatabase('./database.db')
else:
    DB = MySQLDatabase(**config.MYSQL_CONFIG)


class Base(Model):
    class Meta:
        database = DB


class Card(Base):
    id = PrimaryKeyField()
    user_id = CharField()
    side1 = CharField()
    side2 = CharField()

    def __str__(self):
        return f'{self.side1}\n{"="*20}\n{self.side2}'

    def get_labels(self):
        relations = CardLabelRelation.select().join(Label).where(CardLabelRelation.card == self)
        return [relation.label for relation in relations]

    def is_related(self, label):
        relation = CardLabelRelation.get_or_none(card=self, label=label)
        if relation is None:
            return False
        return True

    def get_mem_note(self, user_id):
        return MemNote.get_or_create(card=self, user_id=user_id, defaults={'last_repeating': datetime.now()})[0]

    def can_be_trained(self, user_id):
        note = self.get_mem_note(user_id)
        days_delta = timedelta(note.days_before_repeating - 1)
        if datetime.now() - note.last_repeating > days_delta:
            return True
        return False

    @property
    def short_str(self):
        return f'{self.side1[:10]}{"..." if len(self.side1) >= 10 else ""} / ' \
               f'{self.side2[:10]}{"..." if len(self.side2) >= 10 else ""}'

    def str_with_labels(self):
        labels = self.get_labels()
        if len(labels) == 0:
            return str(self)
        return f'{str(self)}\n\nЗаголовки:\n- ' + "\n- ".join(
            [label.full_str for label in labels]
        )

    def dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'side1': self.side1,
            'side2': self.side2
        }

    class Meta:
        table_name = 'CARDS'


class Label(Base):
    id = PrimaryKeyField()
    user_id = CharField()
    name = CharField()
    is_private = BooleanField(default=False)

    def __str__(self):
        return f'ID {self.id}: {self.name}'

    @property
    def full_str(self):
        return f'ID {self.id}: {self.name} - {"приватный" if self.is_private else "публичный"}'

    def get_cards(self):
        relations = CardLabelRelation.select().join(Card).where(CardLabelRelation.label == self)
        return [relation.card for relation in relations]

    def is_blocked_for_user(self, user_id: int):
        return self.is_private and int(self.user_id) != user_id

    def dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'is_private': self.is_private
        }

    class Meta:
        table_name = 'LABELS'


class CardLabelRelation(Base):
    label = ForeignKeyField(model=Label, backref='relations', on_delete='CASCADE')
    card = ForeignKeyField(model=Card, backref='relations', on_delete='CASCADE')
    is_reversed = BooleanField(default=False)

    def dict(self):
        return {
            'card': self.card.dict(),
            'label': self.label.dict(),
            'is_reversed': self.is_reversed
        }

    class Meta:
        table_name = 'CARDS_LABELS_RELATIONS'


DEFAULT_DAYS_BEFORE_REPEATING_FIRST = 1
DEFAULT_DAYS_BEFORE_REPEATING_SECOND = 6
DEFAULT_EASINESS_FACTOR = 2.5


class MemNote(Base):
    card = ForeignKeyField(model=Card, backref='mem_note', on_delete='CASCADE')
    user_id = CharField()
    last_repeating = DateTimeField()
    days_before_repeating = IntegerField(default=DEFAULT_DAYS_BEFORE_REPEATING_FIRST)
    easiness_factor = FloatField(default=DEFAULT_EASINESS_FACTOR)

    def __str__(self):
        return f'Memory note for card {self.card} and user {self.user_id}: date - {self.last_repeating}; ' \
               f'days delta - {self.days_before_repeating}; EF - {self.easiness_factor}'

    def dict(self):
        return {
            'last_repeating': self.last_repeating,
            'days_before_repeating': self.days_before_repeating,
            'easiness_factor': self.easiness_factor
        }

    class Meta:
        table_name = 'MEM_NOTE'


def create_tables():
    DB.connect()
    DB.create_tables([Card, Label, CardLabelRelation, MemNote])
    DB.close()
