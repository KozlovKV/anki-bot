from core.CRUD import card as CardCRUD
from core.CRUD import label as LabelCRUD
from core.CRUD import memNote as MemNoteCRUD
from core.CRUD import cardLabelRelation as CLR_CRUD

if __name__ == '__main__':
	card1 = CardCRUD.create(1, 'one', 'один')
	card2 = CardCRUD.create(1, 'two', 'два')
	card3 = CardCRUD.create(1, 'three', 'три')
	labelLat = LabelCRUD.create(1, 'digits', 'lat', 'ru')
	labelEng = LabelCRUD.create(1, 'dictionary', 'rus', 'eng')
	CLR_CRUD.create(card1, labelLat)
	CLR_CRUD.create(card2, labelLat)
	CLR_CRUD.create(card2, labelEng)
	CLR_CRUD.create(card3, labelEng)
	print(CLR_CRUD.readAllCardsByLabel(labelLat))
	print(CLR_CRUD.readAllCardsByLabel(labelEng))
	print((CLR_CRUD.readAllLabelsByCard(card1)))
	print((CLR_CRUD.readAllLabelsByCard(card2)))
	CLR_CRUD.delete(card3, labelEng)
	print(CLR_CRUD.readAllCardsByLabel(labelEng))
	CardCRUD.delete(1, card2)
	print(CLR_CRUD.readAllCardsByLabel(labelLat))
	print(CLR_CRUD.readAllCardsByLabel(labelEng))
