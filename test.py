from core.CRUD import card as CardCRUD
from core.CRUD import label as LabelCRUD
from core.CRUD import memNote as MemNoteCRUD
from core.CRUD import cardLabelRelation as CLR_CRUD

from core.anki_engine import AnkiSession

if __name__ == '__main__':
	# c1 = CardCRUD.create(1, 'Hello', 'Привет')
	# c2 = CardCRUD.create(1, 'Hi', 'Привет')
	# c3 = CardCRUD.create(1, 'Bug', 'Баг')
	# c4 = CardCRUD.create(1, 'Bug', 'Жук')
	# c5 = CardCRUD.create(1, 'Chill', 'Прохладный')
	# label = LabelCRUD.create(1, 'Vocabulary', 'Eng', 'Ru')
	# CLR_CRUD.create(c1, label)
	# CLR_CRUD.create(c2, label)
	# CLR_CRUD.create(c3, label)
	# CLR_CRUD.create(c4, label)
	# CLR_CRUD.create(c5, label)
	s = AnkiSession(1)
	s.create_card('test / тест')
