import telebot

import messages

from core import anki_engine


def bind_handlers(bot: telebot.TeleBot):
    bot.register_message_handler(
        get_first_card_side,
        regexp=messages.BASE_BUTTONS[messages.BaseButtonsEnum.ADD_CARD.value],
        pass_bot=True
    )
    bot.register_message_handler(
        show_user_cards,
        regexp=messages.BASE_BUTTONS[messages.BaseButtonsEnum.SHOW_CARDS.value],
        pass_bot=True
    )


def get_first_card_side(message, bot: telebot.TeleBot):
    new_message = bot.send_message(message.chat.id, 'Введите первую сторону карточки')
    bot.register_next_step_handler(new_message, get_second_card_side, bot)


def get_second_card_side(message, bot: telebot.TeleBot):
    new_message = bot.send_message(message.chat.id, 'Введите вторую сторону карточки')
    bot.register_next_step_handler(new_message, create_card, bot, message.text)


def create_card(message, bot: telebot.TeleBot, side1: str):
    card = anki_engine.card_controls.create(message.from_user.id, side1, message.text)
    bot.send_message(
        message.chat.id, 'Карточка успешно создана. Вы можете выбрать заголовок для связывания '
                         'либо сделать что-то другое',
        reply_markup=messages.get_base_markup()
    )


def show_user_cards(message, bot: telebot.TeleBot):
    cards = anki_engine.get_user_cards(message.from_user.id)
    for card in cards:
        bot.send_message(message.chat.id, str(card))
