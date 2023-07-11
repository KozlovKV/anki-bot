ASK_LABEL_ID_PLACEHOLDER = 'ID заголовка для тренировки'
ASK_LABEL_ID_MESSAGE = 'Введите ID заголовка для тренировки ответом на это сообщение (работает один раз)'

NAN_ERROR_MESSAGE = 'Пожалуйста, введите целое положительное число'

NOT_EXIST_LABEL_ID_MESSAGE = 'Заголовка с таким идентификатором не существует'

BLOCKED_LABEL_MESSAGE = 'Извините, но владелец этого заголовка сделал его приватным'

ASK_COUNT_PLACEHOLDER = 'Количество карточек'
ASK_COUNT_MESSAGE = 'Сколько карточек хотите повторить? Введите число ответом на это сообщение (работает один раз)'

EMPTY_TRAIN_LIST = 'Не найдено карточек для тренировки. Отдохните или создайте новые'

TRAIN_LIST_END_MESSAGE = 'Вы можете перейти к началу тренировочного списка по этому реплаю'


def get_train_list_start_message(count: int):
    return f'Найдено карточек для тренировки: {count}'


def get_trainable_card_new_message(card_text: str):
    return f'{card_text}\n\nНасколько хорошо вы помните эту карточку?'


def get_trainable_card_trained_message(old_message, quality):
    return old_message + f'\n\n{quality} - ответ записан'
