import telebot

from bot.base_view import keyboards as base_keyboards


class TrainInlineUrls:
    # request format: "/train/recalculate <card_id> <quality>"
    RECALCULATE = '/train/recalculate '

    # request format "/train/show/side/2 <card_id>"
    SECOND_SIDE = '/train/show/side/2 '


def get_show_second_side_markup(card_id: int):
    inline = telebot.util.quick_markup({
            'Показать вторую сторону': {'callback_data': f'{TrainInlineUrls.SECOND_SIDE}{card_id}'}
    }, row_width=1)
    inline.row(base_keyboards.get_back_menu_button('Закончить тренировку'))
    return inline


def get_quality_markup(card_id: int):
    inline_dict = {}
    for i in range(6):
        inline_dict[str(i)] = {'callback_data': f'{TrainInlineUrls.RECALCULATE}{card_id} {i}'}
    inline = telebot.util.quick_markup(inline_dict, row_width=6)
    inline.row(base_keyboards.get_back_menu_button('Закончить тренировку'))
    return inline
