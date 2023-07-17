FIRST_SIDE_PLACEHOLDER = 'Первая сторона карточки'
FIRST_SIDE_MESSAGE = 'Введите первую сторону карточки ответом на это сообщение. Длина - не более 256 символов'

SECOND_SIDE_PLACEHOLDER = 'Вторая сторона карточки'
SECOND_SIDE_MESSAGE = 'Введите вторую сторону карточки ответом на это сообщение. Длина - не более 256 символов'

CREATE_CARD_SUCCESS = 'Карточка успешно создана'

CARDS_CHOOSING = 'Выберите карточку из списка'

EMPTY_CARDS_LIST = 'У вас пока нет карточек. Скорее создайте первую!'

EDIT_CARD_SUCCESS = 'Карточка успешно изменена'

DELETE_CARD_SUCCESS = 'Карточка удалена'


def get_edit_side_message_dict(side_number):
    return {
        'placeholder': f'Новый текст стороны {side_number}',
        'message': f'Введите новый текст стороны {side_number} ответом на это сообщение. Длина - не более 256 символов'
    }
