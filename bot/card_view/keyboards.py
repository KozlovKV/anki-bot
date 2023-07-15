import telebot

from bot.base_view import keyboards as base_keyboards

from core.anki_engine import Card


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


def get_card_menu_button(card: Card):
    return telebot.types.InlineKeyboardButton(
        card.short_str, callback_data=f'{CardInlinesUrls.BASE_MENU}{card.id}'
    )

def get_cards_choose_inline(
        cards: [Card], back_btn_inline=base_keyboards.get_back_menu_inline(),
        card_btn_function=get_card_menu_button
):
    inline = back_btn_inline
    for card in cards:
        inline.row(card_btn_function(card))
    return inline


def get_base_card_inline(card_id: int):
    inline = telebot.util.quick_markup({
        'Изменить': {'callback_data': f'{CardInlinesUrls.EDIT}{card_id}'},
        'Удалить': {'callback_data': f'{CardInlinesUrls.DELETE}{card_id}'},
        'Настроить связи': {'callback_data': f'{CardInlinesUrls.RELATION}{card_id}'}
    }, row_width=2)
    inline.row(telebot.types.InlineKeyboardButton(
        'В главное меню', callback_data=base_keyboards.BaseMenuUrls.BASE_MENU
    ))
    return inline


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
