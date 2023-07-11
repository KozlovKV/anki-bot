import telebot
from enum import Enum


class LabelInlinesUrls:
    BASE_MENU = '/label/base '

    TRAIN = '/label/train '
    EDIT = '/label/edit '
    DELETE = '/label/delete '
    RELATION = '/label/relations '

    DELETE_PROOF = '/label/delete/proof '

    CREATE_PERMISSION = '/label/create '

    EDIT_PERMISSION = '/label/edit/permission '
    EDIT_NAME = '/label/edit/name '


def get_base_label_inline(label_id: int):
    inline = telebot.types.InlineKeyboardMarkup()
    inline.row(telebot.types.InlineKeyboardButton(
        'Тренироваться', callback_data=f'{LabelInlinesUrls.TRAIN}{label_id}'
    ))
    inline.row(telebot.types.InlineKeyboardButton(
        'Настроить связи', callback_data=f'{LabelInlinesUrls.RELATION}{label_id}'
    ))
    inline.row(
        telebot.types.InlineKeyboardButton(
            'Изменить', callback_data=f'{LabelInlinesUrls.EDIT}{label_id}'
        ),
        telebot.types.InlineKeyboardButton(
            'Удалить', callback_data=f'{LabelInlinesUrls.DELETE}{label_id}'
        )
    )
    return inline


def get_yes_no_inline():
    return telebot.util.quick_markup({
        'Да': {'callback_data': f'{LabelInlinesUrls.CREATE_PERMISSION}{"public"}'},
        'Нет': {'callback_data': f'{LabelInlinesUrls.CREATE_PERMISSION}{"private"}'},
    }, row_width=2)


def get_delete_label_inline(label_id):
    return telebot.util.quick_markup({
        'Подтвердить удаление': {'callback_data': f'{LabelInlinesUrls.DELETE_PROOF}{label_id}'},
        'Назад': {'callback_data': f'{LabelInlinesUrls.BASE_MENU}{label_id}'},
    }, row_width=1)


def get_edit_label_inline(label_id):
    return telebot.util.quick_markup({
        'Переключить режим доступа': {'callback_data': f'{LabelInlinesUrls.EDIT_PERMISSION}{label_id}'},
        'Изменить название': {'callback_data': f'{LabelInlinesUrls.EDIT_NAME}{label_id}'},
        'Назад': {'callback_data': f'{LabelInlinesUrls.BASE_MENU}{label_id}'},
    }, row_width=1)
