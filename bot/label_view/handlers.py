import telebot

import bot.base_view.keyboards as base_keyboards

from .views import LabelView
from . import keyboards


def bind_handlers(bot: telebot.TeleBot):
    bot.register_callback_query_handler(
        handle_create_label_query,
        func=lambda call: base_keyboards.BaseMenuUrls.CREATE_LABEL in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_show_user_labels_query,
        func=lambda call: base_keyboards.BaseMenuUrls.USER_LABELS in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_show_label_query,
        func=lambda call: keyboards.LabelInlinesUrls.BASE_MENU in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_create_label_permission_query,
        func=lambda call: keyboards.LabelInlinesUrls.CREATE_PERMISSION in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_simple_label_delete_query,
        func=lambda call: keyboards.LabelInlinesUrls.DELETE in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        delete_label,
        func=lambda call: keyboards.LabelInlinesUrls.DELETE_PROOF in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_edit_label_query,
        func=lambda call: keyboards.LabelInlinesUrls.EDIT in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_switch_label_permission_query,
        func=lambda call: keyboards.LabelInlinesUrls.EDIT_PERMISSION in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        handle_edit_label_name_query,
        func=lambda call: keyboards.LabelInlinesUrls.EDIT_NAME in call.data,
        pass_bot=True
    )


def handle_create_label_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    LabelView(bot, call=call).ask_private_flag()


def handle_create_label_permission_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    is_private = 'private' in call.data
    bot.register_for_reply(
        LabelView(bot, call=call).ask_label_name(is_private),
        handle_create_label_name_reply, bot, is_private
    )


def handle_create_label_name_reply(message: telebot.types.Message, bot: telebot.TeleBot, is_private: bool):
    LabelView(bot, message=message).create_label(is_private, message.text)


def handle_show_user_labels_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    LabelView(bot, call=call).show_user_labels()


def handle_show_label_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    label_id = int(call.data.split(' ')[1])
    LabelView(bot, call=call).set_base_label_inline(label_id)


def handle_edit_label_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    label_id = int(call.data.split(' ')[1])
    LabelView(bot, call=call).set_edit_label_inline(label_id)


def handle_switch_label_permission_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    label_id = int(call.data.split(' ')[1])
    LabelView(bot, call=call).switch_label_permission(label_id)


def handle_edit_label_name_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    label_id = int(call.data.split(' ')[1])
    bot.register_for_reply(
        LabelView(bot, call=call).ask_new_label_name(),
        handle_edit_label_name_reply, bot, label_id
    )


def handle_edit_label_name_reply(message: telebot.types.Message, bot: telebot.TeleBot, label_id):
    LabelView(bot, message=message).edit_label_name(label_id, message.text)


def handle_simple_label_delete_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    label_id = int(call.data.split(' ')[1])
    LabelView(bot, call=call).ask_label_deletion_proof(label_id)


def delete_label(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    label_id = int(call.data.split(' ')[1])
    LabelView(bot, call=call).delete_label(label_id)
