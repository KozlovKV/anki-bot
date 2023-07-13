import telebot

import bot.card_view.keyboards as card_keyboards


class RelationInlinesUrls:
    # Request format: "/relation/label/switch <label_id> <card_id>"
    SWITCH_LABEL = '/relation/label/switch '

    # Request format: "/relation/card/switch <card_id> <label_id>"
    SWITCH_CARD = '/relation/card/switch '

    # Request format: "/relations/labels/copy <from_label_id> <to_label_id>"
    COPY_RELATIONS_TO = '/relations/labels/copy '


def get_label_switch_inline(label_id):
    return lambda card_id: telebot.util.quick_markup({
        'Связать / отвязать': {'callback_data': f'{RelationInlinesUrls.SWITCH_LABEL}{label_id} {card_id}'}
    })


def get_label_copy_inline(from_label_id: int, labels):
    inline_dict = {}
    for label in labels:
        if label.id != from_label_id:
            inline_dict[str(label)] = {
                'callback_data': f'{RelationInlinesUrls.COPY_RELATIONS_TO}{from_label_id} {label.id}'
            }
    return telebot.util.quick_markup(inline_dict, row_width=1)


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
