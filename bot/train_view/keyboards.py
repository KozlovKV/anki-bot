import telebot


class TrainInlineUrls:
    # request format: "/train/recalculate <card_id> <quality>"
    RECALCULATE = '/train/recalculate '


def get_quality_markup(card_id: int):
    inline_dict = {}
    for i in range(6):
        inline_dict[str(i)] = {'callback_data': f'{TrainInlineUrls.RECALCULATE}{card_id} {i}'}
    return telebot.util.quick_markup(inline_dict, row_width=6)
