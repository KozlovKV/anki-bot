import telebot

from bot import utils

import bot.label_view.handlers as label_handlers

import bot.base_view.keyboards as base_keyboards
import bot.label_view.keyboards as label_keyboards

from core import anki_engine

from . import keyboards
from . import messages


def bind_handlers(bot: telebot.TeleBot):
    bot.register_message_handler(
        ask_label_id,
        regexp=base_keyboards.BaseButtonsEnum.TRAIN.value,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_label_id_from_inline,
        func=lambda call: label_keyboards.LabelInlinesUrls.TRAIN in call.data,
        pass_bot=True
    )
    bot.register_message_handler(
        start_train_from_command,
        commands=['train'],
        pass_bot=True
    )
    bot.register_callback_query_handler(
        recalculate_card,
        func=lambda call: keyboards.TrainInlineUrls.RECALCULATE in call.data,
        pass_bot=True
    )


def ask_label_id(message: telebot.types.Message, bot: telebot.TeleBot):
    new_message = utils.send_message_with_force_reply_placeholder(
        bot, message.chat.id, messages.ASK_LABEL_ID_PLACEHOLDER,
        messages.ASK_LABEL_ID_MESSAGE, reply_to_message_id=message.id
    )
    bot.register_for_reply(new_message, handle_label_id_from_message, bot)


def handle_label_id_from_inline(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    label_id = int(call.data.split(' ')[1])
    ask_count(call.message, bot, label_id)


def check_int(message: telebot.types.Message, bot: telebot.TeleBot, value: any, error_redirect, *args_for_redirect):
    try:
        int_number = int(value)
    except ValueError:
        error_message = bot.send_message(
            message.chat.id, messages.NAN_ERROR_MESSAGE,
            reply_to_message_id=message.id
        )
        error_redirect(error_message, bot, *args_for_redirect)
        return None
    return int_number


def handle_label_id_from_message(message: telebot.types.Message, bot: telebot.TeleBot):
    label_id = check_int(message, bot, message.text, ask_label_id)
    if label_id is None:
        return
    try:
        label = anki_engine.utils.empty_protected_read(anki_engine.Label, label_id)
    except IndexError:
        bot.send_message(
            message.chat.id, messages.NOT_EXIST_LABEL_ID_MESSAGE,
            reply_markup=base_keyboards.get_base_markup(), reply_to_message_id=message.id
        )
        return
    if label.is_blocked_for_user(message.from_user.id):
        bot.send_message(
            message.chat.id, messages.BLOCKED_LABEL_MESSAGE,
            reply_markup=base_keyboards.get_base_markup(), reply_to_message_id=message.id
        )
        return
    label_message = label_handlers.show_label(message.chat.id, bot, label, lambda _: None)
    ask_count(label_message, bot, label_id)


def ask_count(message: telebot.types.Message, bot: telebot.TeleBot, label_id: int):
    new_message = utils.send_message_with_force_reply_placeholder(
        bot, message.chat.id, messages.ASK_COUNT_PLACEHOLDER,
        messages.ASK_COUNT_MESSAGE, reply_to_message_id=message.id
    )
    bot.register_for_reply(new_message, handle_count, bot, label_id)


def handle_count(message: telebot.types.Message, bot: telebot.TeleBot, label_id):
    count = check_int(message, bot, message.text, ask_count, label_id)
    if count is None:
        return
    start_train(message, bot, label_id, count)


def start_train_from_command(message: telebot.types.Message, bot: telebot.TeleBot):
    args = message.text.strip().split(' ')
    label_id = int(args[1])
    count = int(args[2])
    start_train(message, bot, label_id, count)


def start_train(message: telebot.types.Message, bot: telebot.TeleBot, label_id, count):
    train_list = anki_engine.get_cards_to_train(message.from_user.id, label_id, count)
    train(message, bot, train_list)


def show_trainable_card(
        message: telebot.types.Message, bot: telebot.TeleBot,
        trainable_card: anki_engine.Card
):
    bot.send_message(
        message.chat.id, messages.get_trainable_card_new_message(str(trainable_card)),
        reply_markup=keyboards.get_quality_markup(trainable_card.id),
    )


def train(
        message: telebot.types.Message, bot: telebot.TeleBot,  train_list
):
    if len(train_list) == 0:
        bot.send_message(
            message.chat.id, messages.EMPTY_TRAIN_LIST,
            reply_to_message_id=message.id, reply_markup=base_keyboards.get_base_markup()
        )
        return
    start_message = bot.send_message(
        message.chat.id, messages.get_train_list_start_message(len(train_list)),
        reply_to_message_id=message.id
    )
    for card in train_list:
        show_trainable_card(message, bot, card)
    bot.send_message(
        message.chat.id, messages.TRAIN_LIST_END_MESSAGE,
        reply_to_message_id=start_message.id, reply_markup=base_keyboards.get_base_markup()
    )


def recalculate_card(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    data = call.data.split(' ')
    card_id = int(data[1])
    quality = int(data[2])
    anki_engine.recalculate_memory_note(call.from_user.id, card_id, quality)
    new_text_message = messages.get_trainable_card_trained_message(call.message.text, quality)
    bot.edit_message_text(new_text_message, call.message.chat.id, call.message.id, reply_markup=None)
