from core.CRUD import card as CardCRUD
from core.CRUD import label as LabelCRUD
from core.CRUD import memNote as MemNoteCRUD
from core.CRUD import cardLabelRelation as CLR_CRUD

if __name__ == '__main__':
	card1 = CardCRUD.create(1, 'one', 'один')
	memNote = MemNoteCRUD.create(card1, 1)
	MemNoteCRUD.recalculate_memory_note(memNote, 5)
	print(MemNoteCRUD.memNote2Dict(memNote))
	MemNoteCRUD.recalculate_memory_note(memNote, 5)
	print(MemNoteCRUD.memNote2Dict(memNote))
	MemNoteCRUD.recalculate_memory_note(memNote, 5)
	print(MemNoteCRUD.memNote2Dict(memNote))
	MemNoteCRUD.recalculate_memory_note(memNote, 5)
	print(MemNoteCRUD.memNote2Dict(memNote))
	MemNoteCRUD.recalculate_memory_note(memNote, 5)
	print(MemNoteCRUD.memNote2Dict(memNote))
	MemNoteCRUD.recalculate_memory_note(memNote, 5)
	print(MemNoteCRUD.memNote2Dict(memNote))
	MemNoteCRUD.recalculate_memory_note(memNote, 5)
	print(MemNoteCRUD.memNote2Dict(memNote))
	MemNoteCRUD.recalculate_memory_note(memNote, 5)
	print(MemNoteCRUD.memNote2Dict(memNote))
