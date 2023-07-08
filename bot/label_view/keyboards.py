import telebot
from enum import Enum


class LabelInlinesUrls:
    BASE_MENU = '/label/base '

    EDIT = '/label/edit '
    DELETE = '/label/delete '
    RELATION = '/label/relations '

    DELETE_PROOF = '/label/delete/proof '

    CREATE_PERMISSION = '/label/create '


def get_base_label_inline(label_id: int):
    return telebot.util.quick_markup({
        'Изменить': {'callback_data': f'{LabelInlinesUrls.EDIT}{label_id}'},
        'Удалить': {'callback_data': f'{LabelInlinesUrls.DELETE}{label_id}'},
        'Связать с карточками': {'callback_data': f'{LabelInlinesUrls.RELATION}{label_id}'},
    }, row_width=2)


def get_yes_no_inline():
    return telebot.util.quick_markup({
        'Да': {'callback_data': f'{LabelInlinesUrls.CREATE_PERMISSION}{"private"}'},
        'Нет': {'callback_data': f'{LabelInlinesUrls.CREATE_PERMISSION}{"public"}'},
    }, row_width=2)
