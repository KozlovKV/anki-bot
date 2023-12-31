import telebot

from bot.base_view import keyboards as base_keyboards

from core.models import Label


class LabelInlinesUrls:
    BASE_MENU = '/label/base '

    TRAIN = '/label/train '
    EDIT = '/label/edit '
    DELETE = '/label/delete '
    RELATION = '/label/relations '
    COPY_RELATIONS_FROM = '/label/relations/copy '

    DELETE_PROOF = '/label/delete/proof '

    CREATE_PERMISSION = '/label/create/permission '

    EDIT_PERMISSION = '/label/edit/permission '
    EDIT_NAME = '/label/edit/name '


def get_label_back_inline(label_id: int):
    return telebot.util.quick_markup({
        'Вернуться в меню заголовка': {'callback_data': f'{LabelInlinesUrls.BASE_MENU}{label_id}'}
    })


def get_labels_as_inline(labels: [Label]):
    inline_dict = {
        'В главное меню': {'callback_data': base_keyboards.BaseMenuUrls.BASE_MENU}
    }
    for label in labels:
        inline_dict[str(label)] = {
            'callback_data': f'{LabelInlinesUrls.BASE_MENU}{label.id}'
        }
    return telebot.util.quick_markup(inline_dict, row_width=1)


def get_base_label_inline(label_id: int):
    inline = telebot.types.InlineKeyboardMarkup()
    inline.row(telebot.types.InlineKeyboardButton(
        'Тренироваться', callback_data=f'{LabelInlinesUrls.TRAIN}{label_id}'
    ))
    inline.row(
        telebot.types.InlineKeyboardButton(
            'Связи с карточками', callback_data=f'{LabelInlinesUrls.RELATION}{label_id}'
        ),
        telebot.types.InlineKeyboardButton(
            'Скопировать связи', callback_data=f'{LabelInlinesUrls.COPY_RELATIONS_FROM}{label_id}'
        )
    )
    inline.row(
        telebot.types.InlineKeyboardButton(
            'Изменить', callback_data=f'{LabelInlinesUrls.EDIT}{label_id}'
        ),
        telebot.types.InlineKeyboardButton(
            'Удалить', callback_data=f'{LabelInlinesUrls.DELETE}{label_id}'
        )
    )
    inline.row(telebot.types.InlineKeyboardButton(
        'В главное меню', callback_data=base_keyboards.BaseMenuUrls.BASE_MENU
    ))
    return inline


def get_yes_no_inline():
    return telebot.util.quick_markup({
        'Да': {'callback_data': f'{LabelInlinesUrls.CREATE_PERMISSION}{"public"}'},
        'Нет': {'callback_data': f'{LabelInlinesUrls.CREATE_PERMISSION}{"private"}'},
        'Отмена': {'callback_data': base_keyboards.BaseMenuUrls.BASE_MENU}
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
