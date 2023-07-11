import telebot
import os

from core import anki_engine

import bot.base_view.keyboards as base_keyboards
from bot import utils

from . import keyboards
from . import messages

os.path.join('../..')


def bind_handlers(bot: telebot.TeleBot):
    bot.register_message_handler(
        ask_first_card_side,
        regexp=base_keyboards.BaseButtonsEnum.ADD_CARD.value,
        pass_bot=True
    )
    bot.register_message_handler(
        handle_user_id,
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
    new_message = utils.send_message_with_force_reply_placeholder(
        bot, message.chat.id, messages.FIRST_SIDE_PLACEHOLDER,
        messages.FIRST_SIDE_MESSAGE
    )
    bot.register_for_reply(new_message, ask_second_card_side, bot)


def ask_second_card_side(message, bot: telebot.TeleBot):
    new_message = utils.send_message_with_force_reply_placeholder(
        bot, message.chat.id, messages.SECOND_SIDE_PLACEHOLDER,
        messages.SECOND_SIDE_MESSAGE
    )
    bot.register_for_reply(new_message, create_card, bot, message.text)


def create_card(message: telebot.types.Message, bot: telebot.TeleBot, side1: str):
    new_message = bot.send_message(
        message.chat.id, messages.CREATE_CARD_SUCCESS,
        reply_markup=base_keyboards.get_base_markup()
    )
    card = anki_engine.card_controls.create(message.from_user.id, side1, message.text)
    show_card(new_message.chat.id, bot, card)


def handle_user_id(message: telebot.types.Message, bot: telebot.TeleBot):
    show_user_cards(message.chat.id, message.from_user.id, bot)


def show_card(
        chat_id: int, bot: telebot.TeleBot, card: anki_engine.Card,
        markup_function=keyboards.get_base_card_inline
):
    bot.send_message(
        chat_id, card.str_with_labels(),
        reply_markup=markup_function(card.id)
    )


def set_base_card_menu(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    card_id = int(call.data.split(' ')[1])
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.id,
        reply_markup=keyboards.get_base_card_inline(card_id)
    )


def show_user_cards(
        chat_id: int, user_id: int, bot: telebot.TeleBot,
        markup_function=keyboards.get_base_card_inline
):
    cards = anki_engine.get_user_cards(user_id)
    for card in cards:
        show_card(chat_id, bot, card, markup_function)
    if len(cards) == 0:
        bot.send_message(chat_id, messages.EMPTY_CARDS_LIST)


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
    new_message = utils.send_message_with_force_reply_placeholder(
        bot, call.message.chat.id, messages.get_edit_side_placeholder(side_number),
        messages.get_edit_side_message(side_number),
        reply_to_message_id=call.message.id
    )
    bot.register_for_reply(new_message, edit_side, bot, side_number, card_id)


def edit_side(message: telebot.types.Message, bot: telebot.TeleBot, side_number, card_id):
    card = anki_engine.utils.user_protected_read(anki_engine.Card, message.from_user.id, card_id)
    if side_number == 1:
        card.side1 = message.text
    else:
        card.side2 = message.text
    card.save()
    new_message = bot.send_message(
        message.chat.id, messages.EDIT_CARD_SUCCESS,
        reply_markup=base_keyboards.get_base_markup()
    )
    show_card(new_message.chat.id, bot, card)


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
