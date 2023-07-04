from core.CRUD import card as CardCRUD
from core.CRUD import label as LabelCRUD

if __name__ == '__main__':
	# try:
	# 	CardCRUD.delete(17, 17)
	# except PermissionError:
	# 	print('Permission denied')
	# LabelCRUD.create(1, 'ENG/RU', 'ENG', 'RU')
	# LabelCRUD.create(3, 'Tech', 'Definition', 'Value', True)
	# print(LabelCRUD.readOne(1))
	# print(LabelCRUD.readAllUserCards(1))
	# print(LabelCRUD.readAllUserCards(2))
	# print(LabelCRUD.readAllUserCards(3))
	# for i in range(8):
	# 	try:
	# 		LabelCRUD.delete(1, i+1)
	# 	except PermissionError:
	# 		print('Permission denied')
	# print(LabelCRUD.readAllUserCards(1))
	# print(LabelCRUD.readAllUserCards(2))
	# print(LabelCRUD.readAllUserCards(3))
	print(LabelCRUD.readOne(10))
	LabelCRUD.update(3, 10, 'fixed', 'fixed1', 'fixed2')
	print(LabelCRUD.readOne(10))
