FIRST_SIDE_PLACEHOLDER = 'Первая сторона карточки'
FIRST_SIDE_MESSAGE = 'Введите первую сторону карточки ответом на это сообщение (работает один раз)'

SECOND_SIDE_PLACEHOLDER = 'Вторая сторона карточки'
SECOND_SIDE_MESSAGE = 'Введите вторую сторону карточки ответом на это сообщение (работает один раз)'

CREATE_CARD_SUCCESS = 'Карточка успешно создана'

EMPTY_CARDS_LIST = 'У вас пока нет карточек. Скорее создайте первую!'

EDIT_CARD_SUCCESS = 'Карточка успешно изменена'


def get_edit_side_placeholder(side_number):
    return f'Новый текст стороны {side_number}'


def get_edit_side_message(side_number):
    return f'Введите новый текст стороны {side_number} ответом на это сообщение (работает один раз)'
