def get_card_list_end_message(label_str: str):
    return f'Нажимая на кнопки под карточками, вы можете создать или удалить связь с заголовком\n\n{label_str}'


def get_copy_relations_success(from_label: str, to_label: str):
    return f'Связи заголовка {from_label} успешно скопированы заголовку {to_label}'


COPY_RELATIONS_START_MESSAGE = 'Выберите заголовок, которому хотите скопировать связи'

CARD_LIST_START_MESSAGE = 'Начало списка карточек'

CARDS_INLINE_SWITCHING = 'Нажимайте на соответствующие карточкам кнопки для настройки связей'
