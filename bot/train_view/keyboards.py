import telebot


class TrainInlineUrls:
    # request format: "/train/recalculate <card_id> <quality>"
    RECALCULATE = '/train/recalculate '

    # request format "/train/show/side/2 <card_id>"
    SECOND_SIDE = '/train/show/side/2 '


def get_show_second_side_markup(card_id: int):
    return telebot.util.quick_markup(
        {
            'Показать вторую сторону': {'callback_data': f'{TrainInlineUrls.SECOND_SIDE}{card_id}'}
        }, row_width=1
    )


def get_quality_markup(card_id: int):
    inline_dict = {}
    for i in range(6):
        inline_dict[str(i)] = {'callback_data': f'{TrainInlineUrls.RECALCULATE}{card_id} {i}'}
    return telebot.util.quick_markup(inline_dict, row_width=6)
