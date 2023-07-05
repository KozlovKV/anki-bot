from peewee import *

DB_NAME = './database.db'
DB = SqliteDatabase(DB_NAME)


class Base(Model):
    class Meta:
        database = DB


class Card(Base):
    id = PrimaryKeyField()
    user_id = CharField()
    side1 = CharField()
    side2 = CharField()

    def __str__(self):
        return f'{self.side1} / {self.side2}'

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
    side1Name = CharField()
    side2Name = CharField()
    is_private = BooleanField(default=False)

    def __str__(self):
        return f'{self.name}: {self.side1Name} / {self.side2Name} ({"private" if self.is_private else "public"})'

    def dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'side1Name': self.side1Name,
            'side2Name': self.side2Name,
            'is_private': self.is_private
        }

    class Meta:
        table_name = 'LABELS'


class CardLabelRelation(Base):
    label = ForeignKeyField(model=Label, backref='relations', on_delete='CASCADE')
    card = ForeignKeyField(model=Card, backref='relations', on_delete='CASCADE')
    is_reversed = BooleanField(default=False)  # TODO: FIX NAME

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
