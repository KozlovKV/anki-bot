import telebot

import bot.keyboards as base_keyboards

from core import anki_engine

from . import keyboards


def bind_handlers(bot: telebot.TeleBot):
    bot.register_message_handler(
        get_private_flag,
        regexp=base_keyboards.BaseButtonsEnum.ADD_LABEL.value,
        pass_bot=True
    )
    bot.register_message_handler(
        show_user_labels,
        regexp=base_keyboards.BaseButtonsEnum.SHOW_LABELS.value,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        answer_label_name,
        func=lambda call: keyboards.LabelInlinesUrls.CREATE_PERMISSION in call.data,
        pass_bot=True
    )


def get_private_flag(message, bot: telebot.TeleBot):
    bot.send_message(
        message.chat.id, 'Заголовок будет приватным? (другие пользователи не смогут по нему тренироваться)',
        reply_markup=keyboards.get_yes_no_inline()
    )


def answer_label_name(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    new_message = bot.send_message(
        call.message.chat.id, 'Введите название заголовка',
        reply_markup=telebot.types.ReplyKeyboardRemove()
    )
    is_private = 'private' in call.data
    bot.register_next_step_handler(new_message, create_label, bot, is_private)


def create_label(message, bot: telebot.TeleBot, is_private: bool):
    label = anki_engine.label_controls.create(message.from_user.id, message.text, is_private)
    bot.send_message(message.chat.id, 'Заголовок успешно создан.', reply_markup=base_keyboards.get_base_markup())
    show_label(message, bot, label)


def show_label(message: telebot.types.Message, bot: telebot.TeleBot, label: anki_engine.Label):
    bot.send_message(
        message.chat.id, str(label),
        reply_markup=keyboards.get_base_label_inline(label.id)
    )


def show_user_labels(message, bot: telebot.TeleBot):
    labels = anki_engine.get_user_labels(message.from_user.id)
    for label in labels:
        show_label(message, bot, label)
    if len(labels) == 0:
        bot.send_message(message.chat.id, 'У вас пока нет заголовков. Создайте новый!')
