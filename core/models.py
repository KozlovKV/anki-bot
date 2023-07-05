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

	class Meta:
		table_name = 'CARDS'


class Label(Base):
	id = PrimaryKeyField()
	user_id = CharField()
	name = CharField()
	side1Name = CharField()
	side2Name = CharField()
	is_private = BooleanField(default=False)

	class Meta:
		table_name = 'LABELS'


class CardLabelRelation(Base):
	label = ForeignKeyField(model=Label, backref='relations', on_delete='CASCADE')
	card = ForeignKeyField(model=Card, backref='relations', on_delete='CASCADE')
	is_private = BooleanField(default=False)

	class Meta:
		table_name = 'CARDS_LABELS_RELATIONS'


class MemNote(Base):
	card = ForeignKeyField(model=Card, backref='mem_note', on_delete='CASCADE')
	user_id = CharField()
	remembering_moment = DateTimeField()
	memorization_level = IntegerField(default=0)

	class Meta:
		table_name = 'MEM_NOTE'


def create_tables():
	DB.connect()
	DB.create_tables([Card, Label, CardLabelRelation, MemNote])
	DB.close()
