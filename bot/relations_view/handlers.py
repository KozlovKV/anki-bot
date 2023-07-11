import telebot

import bot.base_view.keyboards as base_keyboards

import bot.card_view.handlers as card_handlers
import bot.card_view.keyboards as card_keyboards

import bot.label_view.keyboards as label_keyboards

from . import keyboards

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


def show_cards_for_chaining(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    label_id_for_chaining = int(call.data.split(' ')[1])
    label = anki_engine.utils.user_protected_read(
        anki_engine.Label, call.from_user.id, label_id_for_chaining
    )
    start_message = bot.send_message(
        call.message.chat.id,
        f'Нажимая на кнопки под карточками, вы можете создать или удалить связь с заголовком\n\n{str(label)}'
    )
    card_handlers.show_user_cards(
        call.message.chat.id, call.from_user.id, bot,
        keyboards.get_label_switch_inline(label_id_for_chaining)
    )
    end_message = bot.send_message(
        call.message.chat.id, 'Конец списка карточек. Перейдите в начало по реплаю',
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
    start_message = bot.edit_message_text(
        card.str_with_labels(), message.chat.id, message.id, reply_markup=inline
    )


def handle_card_label_switching(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    data = call.data.split(' ')
    card_id = int(data[1])
    label_id = int(data[2])
    anki_engine.relation_controls.switch_relation(call.from_user.id, card_id, label_id)
    set_labels_inline_for_chaining(call.message, bot, card_id, call.from_user.id)

