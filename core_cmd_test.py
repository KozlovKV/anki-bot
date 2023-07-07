from core import anki_engine

if __name__ == '__main__':
	user_id = int(input('Введите ID: '))
	while True:
		action = int(input("""\
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
			[side1, side2] = input('Введите обе стороны карточки через слэш: ').strip().split('/')
			anki_engine.card_controls.create(user_id, side1, side2)
		elif action == 2:
			cards_list = anki_engine.get_user_cards(user_id)
			if len(cards_list) == 0:
				print('У вас пока нет карточек. Скорее создайте первую!')
			for card in cards_list:
				print(f'Карточка {card.id}:\n {card.str_with_labels()}', end='\n=====\n')
		elif action == 3:
			flag = False if input('Заголовок приватный? (y/n): ').lower().strip() == 'n' else True
			anki_engine.label_controls.create(user_id, input('Введите название заголовка: ').strip(), flag)
		elif action == 4:
			labels_list = anki_engine.get_user_labels(user_id)
			if len(labels_list) == 0:
				print('У вас пока нет заголовков. Создайте новый!')
			for label in labels_list:
				print(f'Заголовок {label.id}: {label}')
		elif action == 5:
			[card_id, label_id] = list(map(
				int, input('Введите ID карточки и заголовка через пробел: ').strip().split()
			))
			anki_engine.relation_controls.create(user_id, card_id, label_id)
		elif action == 6:
			label_id = int(input('Введите ID заголовка: '))
			label = anki_engine.utils.empty_protected_read(anki_engine.Label, label_id)
			cards = label.get_cards()
			if len(cards) == 0:
				print('К этому заголовку пока не привязана ни одна карточка')
			print(*cards, sep='\n', end='\n')
		elif action == 7 or action == 8:
			label_id = int(input('Введите ID заголовка: '))
			train = anki_engine.get_cards_to_train(user_id, label_id)
			for train_card in train:
				q = int(input(f'{train_card} - Оцени уровень памяти от 0 до 5: '))
				anki_engine.recalculate_memory_note(user_id, train_card.id, q)
			if len(train) == 0:
				print('Нечего тренировать, можете отдохнуть )')
		elif action == 9:
			anki_engine.card_controls.delete(user_id, int(input('Введите индекс удаляемой карточки? ')))
		elif action == 10:
			anki_engine.label_controls.delete(user_id, int(input('Введите индекс удаляемого заголовка? ')))
		else:
			break
