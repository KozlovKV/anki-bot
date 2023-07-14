import telebot

from bot import utils

import bot.label_view.handlers as label_handlers

import bot.base_view.keyboards as base_keyboards
import bot.label_view.keyboards as label_keyboards

from core import anki_engine

from .views import TrainView
from . import keyboards
from . import messages
from . import state


def bind_handlers(bot: telebot.TeleBot):
    bot.register_callback_query_handler(
        handle_train_query,
        func=lambda call: base_keyboards.BaseMenuUrls.TRAIN in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_label_id_query,
        func=lambda call: label_keyboards.LabelInlinesUrls.TRAIN in call.data,
        pass_bot=True
    )
    bot.register_message_handler(
        start_train_from_command,
        commands=['train'],
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_show_second_side_query,
        func=lambda call: keyboards.TrainInlineUrls.SECOND_SIDE in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_quality_answer_query,
        func=lambda call: keyboards.TrainInlineUrls.RECALCULATE in call.data,
        pass_bot=True
    )


def handle_train_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    bot.register_for_reply(
        TrainView(bot, call=call).ask_label_id_first_with_canceling_option(),
        handle_label_id_reply, bot
    )


def handle_label_id_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    label_id = int(call.data.split(' ')[1])
    bot.register_for_reply(
        TrainView(bot, call=call).ask_count(),
        handle_count_reply, bot, label_id
    )


def handle_label_id_reply(message: telebot.types.Message, bot: telebot.TeleBot):
    label_id = utils.check_int(message.text)
    view = TrainView(bot, message=message)
    if label_id is None:
        bot.register_for_reply(
            view.send_nan_message(view.ask_label_id),
            handle_label_id_reply, bot
        )
        return
    ask_count_message = view.get_label_from_reply(label_id)
    if ask_count_message is not None:
        bot.register_for_reply(
            ask_count_message,
            handle_count_reply, bot, view.temp_storage['label_id']
        )


def handle_count_reply(message: telebot.types.Message, bot: telebot.TeleBot, label_id):
    count = utils.check_int(message.text)
    view = TrainView(bot, message=message)
    if count is None:
        bot.register_for_reply(
            view.send_nan_message(view.ask_count),
            handle_label_id_reply, bot
        )
        return
    view.start_train(label_id, count)


def start_train_from_command(message: telebot.types.Message, bot: telebot.TeleBot):
    args = message.text.strip().split(' ')
    label_id = int(args[1])
    count = int(args[2])
    TrainView(bot, message=message).start_train(label_id, count)


def handle_show_second_side_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    TrainView(bot, call=call).show_second_side()


def handle_quality_answer_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    data = call.data.split(' ')
    card_id = int(data[1])
    quality = int(data[2])
    TrainView(bot, call=call).recalculate_card(card_id, quality)

