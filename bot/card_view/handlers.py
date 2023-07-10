import telebot
import os

from core import anki_engine

import bot.keyboards as base_keyboards
import bot.utils as utils

import messages
from . import keyboards

os.path.join('../..')


def bind_handlers(bot: telebot.TeleBot):
    bot.register_message_handler(
        ask_first_card_side,
        regexp=base_keyboards.BaseButtonsEnum.ADD_CARD.value,
        pass_bot=True
    )
    bot.register_message_handler(
        show_user_cards,
        regexp=base_keyboards.BaseButtonsEnum.SHOW_CARDS.value,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        set_base_card_menu,
        func=lambda call: keyboards.CardInlinesUrls.BASE_MENU in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        proof_deletion,
        func=lambda call: keyboards.CardInlinesUrls.DELETE in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        delete_card,
        func=lambda call: keyboards.CardInlinesUrls.DELETE_PROOF in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        ask_edit_side,
        func=lambda call: keyboards.CardInlinesUrls.EDIT in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        ask_new_side_text,
        func=lambda call: keyboards.CardInlinesUrls.EDIT_SIDE in call.data,
        pass_bot=True
    )


def ask_first_card_side(message, bot: telebot.TeleBot):
    placeholder = telebot.types.ForceReply(
        input_field_placeholder=f'Первая сторона карточки'
    )
    new_message = bot.send_message(
        message.chat.id, 'Введите первую сторону карточки ответом на это сообщение (работает один раз)',
        reply_markup=placeholder
    )
    bot.register_for_reply(new_message, ask_second_card_side, bot)
    # bot.register_next_step_handler(new_message, ask_second_card_side, bot)


def ask_second_card_side(message, bot: telebot.TeleBot):
    placeholder = telebot.types.ForceReply(
        input_field_placeholder=f'Вторая сторона карточки'
    )
    new_message = bot.send_message(
        message.chat.id, 'Введите вторую сторону карточки ответом на это сообщение (работает один раз)',
        reply_markup=placeholder
    )
    bot.register_for_reply(new_message, create_card, bot, message.text)
    # bot.register_next_step_handler(new_message, create_card, bot, message.text)


def create_card(message: telebot.types.Message, bot: telebot.TeleBot, side1: str):
    new_message = bot.send_message(
        message.chat.id, 'Карточка успешно создана',
        reply_markup=base_keyboards.get_base_markup()
    )
    card = anki_engine.card_controls.create(message.from_user.id, side1, message.text)
    show_card(new_message, bot, card)


def show_card(message: telebot.types.Message, bot: telebot.TeleBot, card: anki_engine.Card):
    bot.send_message(
        message.chat.id, card.str_with_labels(),
        reply_markup=keyboards.get_base_card_inline(card.id)
    )


def set_base_card_menu(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    card_id = int(call.data.split(' ')[1])
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.id,
        reply_markup=keyboards.get_base_card_inline(card_id)
    )


def show_user_cards(message, bot: telebot.TeleBot):
    cards = anki_engine.get_user_cards(message.from_user.id)
    for card in cards:
        show_card(message, bot, card)
    if len(cards) == 0:
        bot.send_message(message.chat.id, 'У вас пока нет карточек. Скорее создайте первую!')


def ask_edit_side(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    card_id = int(call.data.split(' ')[1])
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.id,
        reply_markup=keyboards.get_edit_card_inline(card_id)
    )


def ask_new_side_text(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    data = call.data.split(' ')
    side_number = int(data[0].split('/')[-1])
    card_id = int(data[1])
    placeholder = telebot.types.ForceReply(
        input_field_placeholder=f'Введите новый текст стороны {side_number}'
    )
    new_message = bot.send_message(
        call.message.chat.id, reply_markup=placeholder, reply_to_message_id=call.message.id,
        text=f'Введите новый текст стороны {side_number} ответом на это сообщение',

    )
    bot.register_for_reply(new_message, edit_side, bot, side_number, card_id)
    # bot.register_for_reply(new_message, utils.delete_message_by_handling, bot, new_message)


def edit_side(message: telebot.types.Message, bot: telebot.TeleBot, side_number, card_id):
    card = anki_engine.utils.user_protected_read(anki_engine.Card, message.from_user.id, card_id)
    if side_number == 1:
        card.side1 = message.text
    else:
        card.side2 = message.text
    card.save()
    # bot.delete_message(message.chat.id, message.id, 5)
    new_message = bot.send_message(
        message.chat.id, 'Карточка успешно изменена',
        reply_markup=base_keyboards.get_base_markup()
    )
    show_card(new_message, bot, card)


def proof_deletion(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    card_id = int(call.data.split(' ')[1])
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.id,
        reply_markup=keyboards.get_delete_card_inline(card_id)
    )


def delete_card(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    bot.delete_message(call.message.chat.id, call.message.id)
    card_id = int(call.data.split(' ')[1])
    anki_engine.card_controls.delete(call.from_user.id, card_id)
    bot.answer_callback_query(call.id, 'Карточка успешно удалена')  # TODO: Разобраться, почему не работает
