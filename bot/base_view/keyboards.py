import telebot


class BaseMenuUrls:
    BASE_MENU = '/menu '
    BASE_MENU_NEW = '/menu/new '

    CREATE_CARD = '/card/create '
    CREATE_LABEL = '/label/create '
    USER_CARDS = '/card/show '
    USER_LABELS = '/label/show '
    TRAIN = '/train/start '


def get_base_inline_menu():
    return telebot.util.quick_markup({
        'Добавить карточку': {'callback_data': BaseMenuUrls.CREATE_CARD},
        'Добавить заголовок': {'callback_data': BaseMenuUrls.CREATE_LABEL},
        'Мои карточки': {'callback_data': BaseMenuUrls.USER_CARDS},
        'Мои заголовки': {'callback_data': BaseMenuUrls.USER_LABELS},
        'Тренироваться': {'callback_data': BaseMenuUrls.TRAIN},
    }, row_width=2)


def get_back_menu_inline():
    return telebot.util.quick_markup({
        'Главное меню': {'callback_data': BaseMenuUrls.BASE_MENU}
    })


def get_send_menu_inline():
    return telebot.util.quick_markup({
        'Главное меню': {'callback_data': BaseMenuUrls.BASE_MENU_NEW}
    })
