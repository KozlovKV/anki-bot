import telebot
from enum import Enum


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
        'Связать с заголовками': {'callback_data': f'{CardInlinesUrls.RELATION}{card_id}'},
    }, row_width=2)


def get_edit_card_inline(card_id):
    return telebot.util.quick_markup({
        'Изменить первую сторону': {'callback_data': f'{CardInlinesUrls.EDIT_SIDE}{1} {card_id}'},
        'Изменить вторую сторону': {'callback_data': f'{CardInlinesUrls.EDIT_SIDE}{2} {card_id}'},
        'Отменить редактирование': {'callback_data': f'{CardInlinesUrls.BASE_MENU}{card_id}'},
    }, row_width=2)


def get_delete_card_inline(card_id):
    return telebot.util.quick_markup({
        'Подтвердить удаление': {'callback_data': f'{CardInlinesUrls.DELETE_PROOF}{card_id}'},
        'Отмена': {'callback_data': f'{CardInlinesUrls.BASE_MENU}{card_id}'},
    }, row_width=1)
