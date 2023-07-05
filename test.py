from core.CRUD import card as CardCRUD
from core.CRUD import label as LabelCRUD
from core.CRUD import memNote as MemNoteCRUD

if __name__ == '__main__':
	card = CardCRUD.Card.get(id=5)
	note = MemNoteCRUD.create(card, 1)
	MemNoteCRUD.change_memorization_level(note, 5)
	print(MemNoteCRUD.memNote2Dict(note))
	MemNoteCRUD.change_memorization_level(note, 5)
	print(MemNoteCRUD.memNote2Dict(note))
	MemNoteCRUD.change_memorization_level(note, 5)
	print(MemNoteCRUD.memNote2Dict(note))
	MemNoteCRUD.change_memorization_level(note, -5)
	print(MemNoteCRUD.memNote2Dict(note))
	MemNoteCRUD.change_memorization_level(note, -10)
	print(MemNoteCRUD.memNote2Dict(note))
	MemNoteCRUD.change_memorization_level(note, -10)
	print(MemNoteCRUD.memNote2Dict(note))
	MemNoteCRUD.delete(card, 1)
	print(MemNoteCRUD.readOne(card, 1))