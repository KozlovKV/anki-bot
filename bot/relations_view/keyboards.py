import telebot

import bot.card_view.keyboards as card_keyboards


class RelationInlinesUrls:
    SWITCH_LABEL = '/relation/label/switch '
    SWITCH_CARD = '/relation/card/switch '


def get_label_switch_inline(label_id):
    return lambda card_id: telebot.util.quick_markup({
        'Связать / отвязать': {'callback_data': f'{RelationInlinesUrls.SWITCH_LABEL}{label_id} {card_id}'}
    })


def get_card_switch_inline(card_id: int, labels):
    inline_dict = {}
    for label in labels:
        inline_dict[str(label)] = {
            'callback_data': f'{RelationInlinesUrls.SWITCH_CARD}{card_id} {label.id}'
        }
    inline_dict['Назад'] = {
        'callback_data': f'{card_keyboards.CardInlinesUrls.BASE_MENU}{card_id}'
    }
    return telebot.util.quick_markup(inline_dict, row_width=1)
