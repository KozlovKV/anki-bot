import telebot

from bot import utils

import bot.base_view.keyboards as base_keyboards

import bot.card_view.handlers as card_handlers
import bot.card_view.keyboards as card_keyboards

import bot.label_view.handlers as label_handlers
import bot.label_view.keyboards as label_keyboards

from . import keyboards
from . import messages

from core import anki_engine


def bind_handlers(bot: telebot.TeleBot):
    bot.register_message_handler(
        create_relation_from_command,
        commands=['chain'],
        pass_bot=True
    )
    bot.register_callback_query_handler(
        show_cards_for_chaining,
        func=lambda call: label_keyboards.LabelInlinesUrls.RELATION in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_label_card_switching,
        func=lambda call: keyboards.RelationInlinesUrls.SWITCH_LABEL in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_card_chaining,
        func=lambda call: card_keyboards.CardInlinesUrls.RELATION in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_card_label_switching,
        func=lambda call: keyboards.RelationInlinesUrls.SWITCH_CARD in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        ask_from_label_id,
        func=lambda call: label_keyboards.LabelInlinesUrls.COPY_RELATIONS_FROM in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_to_from_label_id,
        func=lambda call: keyboards.RelationInlinesUrls.COPY_RELATIONS_TO in call.data,
        pass_bot=True
    )


# TODO: Удалить блок ниже либо оставить только для админа
def create_relation(message, bot: telebot.TeleBot, card_id: int, label_id: int):
    card = anki_engine.utils.user_protected_read(anki_engine.Card, message.from_user.id, card_id)
    label = anki_engine.utils.user_protected_read(anki_engine.Label, message.from_user.id, label_id)
    relation = anki_engine.relation_controls.create_by_instances(message.from_user.id, card, label)
    text = f'Карточка\n\n {card}\n\nУспешно связана с заголовком\n\n {label}' \
        if relation[1] else \
        f'Связь между карточкой\n\n {card}\nИ заголовком\n\n {label}\n\nуже есть'
    bot.send_message(
        message.chat.id, text, reply_markup=base_keyboards.get_base_markup()
    )


def create_relation_from_command(message, bot: telebot.TeleBot):
    args = message.text.strip().split(' ')
    card_id = int(args[1])
    label_id = int(args[2])
    create_relation(message, bot, card_id, label_id)
# TODO: конец блока на удаление


def show_cards_for_chaining(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    label_id_for_chaining = int(call.data.split(' ')[1])
    label = anki_engine.utils.user_protected_read(
        anki_engine.Label, call.from_user.id, label_id_for_chaining
    )
    start_message = bot.send_message(
        call.message.chat.id, messages.get_card_list_start_message(str(label))
    )
    card_handlers.show_user_cards(
        call.message.chat.id, call.from_user.id, bot,
        keyboards.get_label_switch_inline(label_id_for_chaining)
    )
    bot.send_message(
        call.message.chat.id, messages.CARD_LIST_END_MESSAGE,
        reply_to_message_id=start_message.id
    )


def handle_label_card_switching(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    data = call.data.split(' ')
    label_id = int(data[1])
    card_id = int(data[2])
    anki_engine.relation_controls.switch_relation(call.from_user.id, card_id, label_id)

    card = anki_engine.utils.user_protected_read(anki_engine.Card, call.from_user.id, card_id)
    bot.edit_message_text(
        card.str_with_labels(), call.message.chat.id, call.message.id,
        reply_markup=keyboards.get_label_switch_inline(label_id)(card_id)
    )


def handle_card_chaining(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    card_id = int(call.data.split(' ')[1])
    user_id = call.from_user.id
    set_labels_inline_for_chaining(call.message, bot, card_id, user_id)


def set_labels_inline_for_chaining(message: telebot.types.Message, bot: telebot.TeleBot, card_id, user_id):
    card = anki_engine.utils.user_protected_read(anki_engine.Card, user_id, card_id)
    labels = anki_engine.get_user_labels(user_id)
    inline = keyboards.get_card_switch_inline(card_id, labels)
    bot.edit_message_text(card.str_with_labels(), message.chat.id, message.id, reply_markup=inline)


def handle_card_label_switching(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    data = call.data.split(' ')
    card_id = int(data[1])
    label_id = int(data[2])
    anki_engine.relation_controls.switch_relation(call.from_user.id, card_id, label_id)
    set_labels_inline_for_chaining(call.message, bot, card_id, call.from_user.id)


def ask_from_label_id(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    from_label_id = int(call.data.split(' ')[1])
    labels = anki_engine.get_user_labels(call.from_user.id)
    bot.send_message(
        call.message.chat.id, messages.COPY_RELATIONS_START_MESSAGE,
        reply_to_message_id=call.message.id,
        reply_markup=keyboards.get_label_copy_inline(from_label_id, labels)
    )


def handle_to_from_label_id(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    data = call.data.split(' ')
    from_label_id = int(data[1])
    to_label_id = int(data[2])
    bot.delete_message(call.message.chat.id, call.message.message_id)

    anki_engine.relation_controls.copy_relation_from_other_label(call.from_user.id, to_label_id, from_label_id)
    to_label = anki_engine.utils.user_protected_read(anki_engine.Label, call.from_user.id, to_label_id)
    from_label = anki_engine.utils.user_protected_read(anki_engine.Label, call.from_user.id, from_label_id)
    bot.send_message(
        call.message.chat.id, messages.get_copy_relations_success(to_label.name, from_label.name),
        reply_markup=base_keyboards.get_base_markup()
    )
