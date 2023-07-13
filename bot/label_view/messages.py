IS_PUBLIC_MESSAGE = 'Сделать доступной тренировку по этому заголовку всем желающим ' \
                    '(без возможности какого-либо редактирования)'

CREATE_LABEL_SUCCESS = 'Заголовок успешно создан'

CHOOSE_LABEL = 'Выберите заголовок для работы с ним'

EMPTY_LABELS_LIST = 'У вас пока нет заголовков. Создайте новый!'

EDIT_LABEL_NAME_PLACEHOLDER = 'Новое название заголовка'
EDIT_LABEL_NAME_MESSAGE = 'Введите новое название заголовка ответом на это сообщение (Работает один раз)'
EDIT_LABEL_NAME_SUCCESS = 'Название заголовка изменено'


def get_label_name_message_dict(is_private: bool):
    is_private_str = 'приватного' if is_private else 'публичного'
    return {
        'placeholder': f'Название {is_private_str} заголовка',
        'message': f'Введите название {is_private_str} заголовка ответом на это сообщение (работает один раз)',
    }
