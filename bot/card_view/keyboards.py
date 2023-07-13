import telebot

from bot.base_view import keyboards as base_keyboards


class CardInlinesUrls:
    # For canceling
    BASE_MENU = '/card/base '

    # Base menu
    EDIT = '/card/edit '
    DELETE = '/card/delete '
    RELATION = '/card/relations '

    DELETE_PROOF = '/card/delete/proof '

    # Edit variants (like "/card/edit/<side_number>")
    EDIT_SIDE = '/card/edit/'


def get_base_card_inline(card_id: int):
    return telebot.util.quick_markup({
        'Изменить': {'callback_data': f'{CardInlinesUrls.EDIT}{card_id}'},
        'Удалить': {'callback_data': f'{CardInlinesUrls.DELETE}{card_id}'},
        'Настроить связи': {'callback_data': f'{CardInlinesUrls.RELATION}{card_id}'},
        'В главное меню': {'callback_data': base_keyboards.BaseMenuUrls.BASE_MENU}
    }, row_width=2)


def get_edit_card_inline(card_id):
    return telebot.util.quick_markup({
        'Сторона 1': {'callback_data': f'{CardInlinesUrls.EDIT_SIDE}{1} {card_id}'},
        'Сторона 2': {'callback_data': f'{CardInlinesUrls.EDIT_SIDE}{2} {card_id}'},
        'Назад': {'callback_data': f'{CardInlinesUrls.BASE_MENU}{card_id}'},
    }, row_width=2)


def get_delete_card_inline(card_id):
    return telebot.util.quick_markup({
        'Подтвердить удаление': {'callback_data': f'{CardInlinesUrls.DELETE_PROOF}{card_id}'},
        'Назад': {'callback_data': f'{CardInlinesUrls.BASE_MENU}{card_id}'},
    }, row_width=1)
