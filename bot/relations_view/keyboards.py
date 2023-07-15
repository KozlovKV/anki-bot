import telebot

import bot.card_view.keyboards as card_keyboards
import bot.label_view.keyboards as label_keyboards

from core.models import Label, Card


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


def get_label_card_switch_inline_btn(label: Label):
    return lambda card: telebot.types.InlineKeyboardButton(
        f'{card.short_str} - {"Привязана" if card.is_related(label) else "Не привязана"}',
        callback_data=f'{RelationInlinesUrls.SWITCH_LABEL}{label.id} {card.id}'
    )


def get_label_to_cards_switch_inline(label: Label, cards: [Card]):
    return card_keyboards.get_cards_choose_inline(
        cards, label_keyboards.get_label_back_inline(label.id),
        get_label_card_switch_inline_btn(label)
    )


def get_label_copy_inline(from_label_id: int, labels: [Label]):
    inline_dict = {
        'Отмена': {'callback_data': f'{label_keyboards.LabelInlinesUrls.BASE_MENU}{from_label_id}'}
    }
    for label in labels:
        if label.id != from_label_id:
            inline_dict[str(label)] = {
                'callback_data': f'{RelationInlinesUrls.COPY_RELATIONS_TO}{from_label_id} {label.id}'
            }
    return telebot.util.quick_markup(inline_dict, row_width=1)


def get_card_switch_inline(card_id: int, labels: [Label]):
    inline_dict = {
        'Назад': {'callback_data': f'{card_keyboards.CardInlinesUrls.BASE_MENU}{card_id}'}
    }
    for label in labels:
        inline_dict[str(label)] = {
            'callback_data': f'{RelationInlinesUrls.SWITCH_CARD}{card_id} {label.id}'
        }
    return telebot.util.quick_markup(inline_dict, row_width=1)
