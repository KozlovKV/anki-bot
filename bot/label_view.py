import telebot

import messages

from core import anki_engine


def bind_handlers(bot: telebot.TeleBot):
    bot.register_message_handler(
        get_private_flag,
        regexp=messages.BASE_BUTTONS[messages.BaseButtonsEnum.ADD_LABEL.value],
        pass_bot=True
    )
    bot.register_message_handler(
        show_user_labels,
        regexp=messages.BASE_BUTTONS[messages.BaseButtonsEnum.SHOW_LABELS.value],
        pass_bot=True
    )


def get_private_flag(message, bot: telebot.TeleBot):
    new_message = bot.send_message(
        message.chat.id, 'Заголовок будет приватным? (другие пользователи не смогут по нему тренироваться)',
        reply_markup=messages.get_yes_no_markup()
    )
    bot.register_next_step_handler(new_message, get_label_name, bot)


def get_label_name(message, bot: telebot.TeleBot):
    new_message = bot.send_message(
        message.chat.id, 'Введите название заголовка',
        reply_markup=telebot.types.ReplyKeyboardRemove()
    )
    is_private = message.text == 'Да'
    bot.register_next_step_handler(new_message, create_label, bot, is_private)


def create_label(message, bot: telebot.TeleBot, is_private: bool):
    label = anki_engine.label_controls.create(message.from_user.id, message.text, is_private)
    bot.send_message(message.chat.id, 'Заголовок успешно создан.', reply_markup=messages.get_base_markup())


def show_user_labels(message, bot: telebot.TeleBot):
    labels = anki_engine.get_user_labels(message.from_user.id)
    for label in labels:
        bot.send_message(message.chat.id, str(label))
    if len(labels) == 0:
        bot.send_message(message.chat.id, 'У вас пока нет заголовков. Создайте новый!')
