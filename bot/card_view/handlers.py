import telebot
import os

from bot.base_view import keyboards as base_keyboards

from .views import CardView
from . import keyboards

os.path.join('../..')


def bind_handlers(bot: telebot.TeleBot):
    bot.register_callback_query_handler(
        handle_create_card_query,
        func=lambda call: base_keyboards.BaseMenuUrls.CREATE_CARD in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_user_id,
        func=lambda call: base_keyboards.BaseMenuUrls.USER_CARDS in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_base_card_menu_query,
        func=lambda call: keyboards.CardInlinesUrls.BASE_MENU in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_simple_card_delete_query,
        func=lambda call: keyboards.CardInlinesUrls.DELETE in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_delete_card_query,
        func=lambda call: keyboards.CardInlinesUrls.DELETE_PROOF in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_card_edit_query,
        func=lambda call: keyboards.CardInlinesUrls.EDIT in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_edit_side_number_query,
        func=lambda call: keyboards.CardInlinesUrls.EDIT_SIDE in call.data,
        pass_bot=True
    )


def handle_create_card_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    bot.register_for_reply(
        CardView(bot, call=call).ask_first_card_side(),
        handle_first_card_side, bot
    )


def handle_first_card_side(message: telebot.types.Message, bot: telebot.TeleBot):
    bot.register_for_reply(
        CardView(bot, message=message).ask_second_card_side(),
        handle_second_card_side, bot, message.text
    )


def handle_second_card_side(message: telebot.types.Message, bot: telebot.TeleBot, side1: str):
    CardView(bot, message=message).create_card(side1, message.text)


def handle_user_id(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    CardView(bot, call=call).send_user_cards()


def handle_base_card_menu_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    card_id = int(call.data.split(' ')[1])
    CardView(bot, call=call).set_base_card_menu_inline(card_id)


def handle_card_edit_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    card_id = int(call.data.split(' ')[1])
    CardView(bot, call=call).set_edit_side_inline(card_id)


def handle_edit_side_number_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    data = call.data.split(' ')
    side_number = int(data[0].split('/')[-1])
    card_id = int(data[1])
    bot.register_for_reply(
        CardView(bot, call=call).ask_new_side_text(side_number),
        handle_new_side_text_reply, bot, side_number, card_id
    )


def handle_new_side_text_reply(message: telebot.types.Message, bot: telebot.TeleBot, side_number, card_id):
    CardView(bot, message=message).edit_side(card_id, side_number, message.text)


def handle_simple_card_delete_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    card_id = int(call.data.split(' ')[1])
    CardView(bot, call=call).ask_deletion_proof(card_id)


def handle_delete_card_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    card_id = int(call.data.split(' ')[1])
    CardView(bot, call=call).delete_card(card_id)
