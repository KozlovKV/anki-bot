import telebot

import messages

from core import anki_engine


def bind_handlers(bot: telebot.TeleBot):
    bot.register_message_handler(
        ask_label_id,
        regexp=messages.BASE_BUTTONS[messages.BaseButtonsEnum.TRAIN.value],
        pass_bot=True
    )
    bot.register_message_handler(
        start_train_from_command,
        commands=['train'],
        pass_bot=True
    )


def ask_label_id(message, bot: telebot.TeleBot):
    new_message = bot.send_message(message.chat.id, 'Введите ID заголовка для тренировки')
    bot.register_next_step_handler(new_message, handle_label_id, bot)


def handle_label_id(message, bot: telebot.TeleBot):
    label_id = int(message.text)
    new_message = bot.send_message(
        message.chat.id, 'Сколько карточек хотите повторить?',
        reply_markup=messages.get_count_markup()
    )
    bot.register_next_step_handler(new_message, handle_count, bot, label_id)


# TODO: Добавить валидацию по правам доступа, наличию номера и корректности ввода (число)
def handle_count(message, bot: telebot.TeleBot, label_id):
    count = int(message.text)
    start_train(message, bot, label_id, count)


def start_train_from_command(message, bot: telebot.TeleBot):
    args = message.text.strip().split(' ')
    label_id = int(args[1])
    count = int(args[2])
    start_train(message, bot, label_id, count)


def start_train(message, bot: telebot.TeleBot, label_id, count):
    train_list = anki_engine.get_cards_to_train(message.from_user.id, label_id, count)
    train(message, bot, train_list)


def train(message, bot, train_list, is_initial=True, current_card=None):
    if not is_initial:
        anki_engine.recalculate_memory_note(message.from_user.id, current_card.id, int(message.text))
    if len(train_list) == 0:
        bot.send_message(
            message.chat.id, 'Карточки закончились. Отдохните ;)',
            reply_markup=messages.get_base_markup()
        )
        return
    new_message = bot.send_message(
        message.chat.id, f'{str(train_list[0])}\n\nНасколько хорошо вы помните эту карточку?',
        reply_markup=messages.get_quality_markup()
    )
    bot.register_next_step_handler(new_message, train, bot, train_list[1:], False, train_list[0])

