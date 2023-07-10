import telebot

import bot.keyboards as base_keyboards
from bot import utils

from core import anki_engine

from . import keyboards


def bind_handlers(bot: telebot.TeleBot):
    bot.register_message_handler(
        ask_label_id,
        regexp=base_keyboards.BaseButtonsEnum.TRAIN.value,
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
        bot, message.chat.id, 'ID заголовка для тренировки',
        'Введите ID заголовка для тренировки ответом на это сообщение (работает один раз)',
        reply_to_message_id=message.id
    )
    bot.register_for_reply(new_message, ask_count, bot)


def ask_count(message: telebot.types.Message, bot: telebot.TeleBot):
    label_id = int(message.text)
    new_message = utils.send_message_with_force_reply_placeholder(
        bot, message.chat.id, 'Количество карточек',
        'Сколько карточек хотите повторить? Введите число ответом на это сообщение (работает один раз)',
        reply_to_message_id=message.id
    )
    bot.register_for_reply(new_message, handle_count, bot, label_id)


# TODO: Добавить валидацию по правам доступа, наличию номера и корректности ввода (число)
def handle_count(message: telebot.types.Message, bot: telebot.TeleBot, label_id):
    count = int(message.text)
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
        message.chat.id, f'{str(trainable_card)}\n\nНасколько хорошо вы помните эту карточку?',
        reply_markup=keyboards.get_quality_markup(trainable_card.id)
    )


def train(
        message: telebot.types.Message, bot: telebot.TeleBot,
        train_list
):
    if len(train_list) == 0:
        end_message = bot.send_message(
            message.chat.id, 'Не найдено карточек для тренировки. Отдохните или создайте новые',
            reply_to_message_id=message.id, reply_markup=base_keyboards.get_base_markup()
        )
        return
    bot.send_message(
        message.chat.id, f'Для тренировки найдено {len(train_list)} карточек',
        reply_to_message_id=message.id
    )
    start_message = bot.send_message(message.chat.id, 'Начало тренировки')
    for card in train_list:
        show_trainable_card(message, bot, card)
    end_message = bot.send_message(
        message.chat.id, 'Вы можете перейти к началу тренировочного списка по этому реплаю',
        reply_to_message_id=start_message.id, reply_markup=base_keyboards.get_base_markup()
    )
    # if not is_initial:
    #     anki_engine.recalculate_memory_note(message.from_user.id, current_card.id, int(message.text))
    # if len(train_list) == 0:
    #     bot.send_message(
    #         message.chat.id, 'Карточки закончились. Отдохните ;)',
    #         reply_markup=base_keyboards.get_base_markup()
    #     )
    #     return
    # new_message = bot.send_message(
    #     message.chat.id, f'{str(train_list[0])}\n\nНасколько хорошо вы помните эту карточку?',
    #     reply_markup=base_keyboards.get_quality_markup()
    # )
    # bot.register_next_step_handler(new_message, train, bot, train_list[1:], False, train_list[0])


def recalculate_card(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    data = call.data.split(' ')
    card_id = int(data[1])
    quality = int(data[2])
    anki_engine.recalculate_memory_note(call.from_user.id, card_id, quality)
    new_text_message = call.message.text + f'\n\n{quality} - ответ записан'
    bot.edit_message_text(new_text_message, call.message.chat.id, call.message.id, reply_markup=None)
