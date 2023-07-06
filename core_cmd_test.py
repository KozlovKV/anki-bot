from core.CRUD import card as CardCRUD
from core.CRUD import label as LabelCRUD
from core.CRUD import memNote as MemNoteCRUD
from core.CRUD import cardLabelRelation as CLR_CRUD

from core.anki_engine import AnkiSession

if __name__ == '__main__':
	user_id = int(input('Введите ID: '))
	s = AnkiSession(user_id)
	while True:
		action = int(input("""
1. Добавить карточку
2. Вывести мои карточки
3. Добавить заголовок
4. Вывести мои заголовки
5. Связать карточку с заголовком
6. Показать карточки по заголовку
7. Начать тренировку по своим заголовкам
8. Начать тренировку по произвольному заголовку
9. Удалить карточку
10. Удалить заголовок
Другой ввод - завершить сессию
"""))
		if action == 1:
			s.create_card(input('Введите обе стороны карточки через слэш: ').strip())
		elif action == 2:
			if len(s.cards_list) == 0:
				print('У вас пока нет карточек. Скорее создайте!')
			for i in range(len(s.cards_list)):
				print(f'Карточка {i}:\n {s.get_full_card_info_str(i)}', end='\n=====\n')
		elif action == 3:
			flag = False if input('Заголовок приватный? (y/n): ').lower().strip() == 'n' else True
			s.create_label(input('Введите название заголовка: ').strip(), flag)
		elif action == 4:
			if len(s.labels_list) == 0:
				print('У вас пока нет заголовков. Создайте новый!')
			for i in range(len(s.labels_list)):
				print(f'Заголовок {i}: {s.labels_list[i]}')
		elif action == 5:
			[card_index, label_index] = list(map(
				int, input('Введите индекс карточки и заголовка через пробел: ').strip().split()
			))
			s.create_relation(card_index, label_index)
		elif action == 6:
			print('')
			label_index = int(input('Введите индекс заголовка: '))
			cards = s.labels_list[label_index].get_cards()
			if len(cards) == 0:
				print('К этому заголовку пока не привязана ни одна карточка')
			print(*cards, sep='\n', end='\n')
		elif action == 7 or action == 8:
			label = None
			if action == 7:
				label_index = int(input('Введите индекс своего заголовка: '))
				label = s.labels_list[label_index]
			else:
				label_id = int(input('Введите ID заголовка (не индексы из вашего списка!) '))
				label = LabelCRUD.Label.get_or_none(id=label_id)
			train = s.get_cards_to_train(label)
			i = 0
			for train_card in train:
				q = int(input(f'{train_card[0]} - Оцени уровень памяти от 0 до 5: '))
				s.recalculate_memory_note(i, q)
				i += 1
			if len(train) == 0:
				print('Нечего тренировать, можете отдохнуть )')
		elif action == 9:
			s.delete_card(int(input('Введите индекс удаляемой карточки? ')))
		elif action == 10:
			s.delete_label(int(input('Введите индекс удаляемого заголовка? ')))
		else:
			break
