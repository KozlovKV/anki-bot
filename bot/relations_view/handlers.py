import telebot

import bot.card_view.keyboards as card_keyboards
import bot.label_view.keyboards as label_keyboards

from .views import RelationView
from . import keyboards


def bind_handlers(bot: telebot.TeleBot):
    bot.register_callback_query_handler(
        handle_label_to_cards_relations_editing_query,
        func=lambda call: label_keyboards.LabelInlinesUrls.RELATION in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_switch_label_card_query,
        func=lambda call: keyboards.RelationInlinesUrls.SWITCH_LABEL in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_card_to_labels_editing_query,
        func=lambda call: card_keyboards.CardInlinesUrls.RELATION in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_switch_card_label_query,
        func=lambda call: keyboards.RelationInlinesUrls.SWITCH_CARD in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_copy_relation_from_query,
        func=lambda call: label_keyboards.LabelInlinesUrls.COPY_RELATIONS_FROM in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_copy_relation_to_query,
        func=lambda call: keyboards.RelationInlinesUrls.COPY_RELATIONS_TO in call.data,
        pass_bot=True
    )


def handle_label_to_cards_relations_editing_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    label_id = int(call.data.split(' ')[1])
    RelationView(bot, call=call).send_cards_for_chaining_to_label(label_id)


def handle_switch_label_card_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    data = call.data.split(' ')
    label_id = int(data[1])
    card_id = int(data[2])
    RelationView(bot, call=call).switch_label_card_relation(label_id, card_id)


def handle_card_to_labels_editing_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    card_id = int(call.data.split(' ')[1])
    RelationView(bot, call=call).set_card_labels_inline_for_chaining(card_id)


def handle_switch_card_label_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    data = call.data.split(' ')
    card_id = int(data[1])
    label_id = int(data[2])
    RelationView(bot, call=call).switch_card_label_relation(card_id, label_id)


def handle_copy_relation_from_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    from_label_id = int(call.data.split(' ')[1])
    RelationView(bot, call=call).set_label_copy_relations_inline(from_label_id)


def handle_copy_relation_to_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    data = call.data.split(' ')
    from_label_id = int(data[1])
    to_label_id = int(data[2])
    RelationView(bot, call=call).copy_relations(from_label_id, to_label_id)
