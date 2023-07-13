import telebot

import bot.base_view.keyboards as base_keyboards
from bot import utils

from core import anki_engine

from . import keyboards
from . import messages


def bind_handlers(bot: telebot.TeleBot):
    bot.register_message_handler(
        ask_private_flag,
        regexp=base_keyboards.BaseButtonsEnum.ADD_LABEL.value,
        pass_bot=True
    )
    bot.register_message_handler(
        show_user_labels_by_message,
        regexp=base_keyboards.BaseButtonsEnum.SHOW_LABELS.value,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        set_base_label_menu,
        func=lambda call: keyboards.LabelInlinesUrls.BASE_MENU in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        ask_label_name,
        func=lambda call: keyboards.LabelInlinesUrls.CREATE_PERMISSION in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        proof_deletion,
        func=lambda call: keyboards.LabelInlinesUrls.DELETE in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        delete_label,
        func=lambda call: keyboards.LabelInlinesUrls.DELETE_PROOF in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        show_edit_inline,
        func=lambda call: keyboards.LabelInlinesUrls.EDIT in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        switch_label_permission,
        func=lambda call: keyboards.LabelInlinesUrls.EDIT_PERMISSION in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        ask_new_label_name,
        func=lambda call: keyboards.LabelInlinesUrls.EDIT_NAME in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        show_user_labels_by_query,
        func=lambda call: keyboards.LabelInlinesUrls.CHOOSE_LABELS in call.data,
        pass_bot=True
    )


def ask_private_flag(message: telebot.types.Message, bot: telebot.TeleBot):
    bot.send_message(
        message.chat.id, messages.IS_PUBLIC_MESSAGE,
        reply_markup=keyboards.get_yes_no_inline()
    )


def ask_label_name(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    bot.delete_message(call.message.chat.id, call.message.id)
    is_private = 'private' in call.data
    message_dict = messages.get_label_name_message_dict(is_private)
    new_message = utils.send_message_with_force_reply_placeholder(
        bot, call.message.chat.id, message_dict['placeholder'],
        message_dict['message']
    )
    bot.register_for_reply(new_message, create_label, bot, is_private)


def create_label(message: telebot.types.Message, bot: telebot.TeleBot, is_private: bool):
    label = anki_engine.label_controls.create(message.from_user.id, message.text, is_private)
    bot.send_message(
        message.chat.id, messages.CREATE_LABEL_SUCCESS,
        reply_markup=base_keyboards.get_base_markup()
    )
    show_label(message.chat.id, bot, label)


def show_user_labels_by_message(message: telebot.types.Message, bot: telebot.TeleBot):
    bot.send_message(
        message.chat.id, messages.CHOOSE_LABEL,
        reply_markup=keyboards.get_labels_as_inline(
            anki_engine.get_user_labels(message.from_user.id)
        )
    )
    bot.delete_message(message.chat.id, message.id)


def show_user_labels_by_query(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    print(call.message.text)
    bot.edit_message_text(
        messages.CHOOSE_LABEL,
        call.message.chat.id, call.message.id,
        reply_markup=keyboards.get_labels_as_inline(
            anki_engine.get_user_labels(call.from_user.id)
        )
    )


def set_base_label_menu(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    label_id = int(call.data.split(' ')[1])
    label = anki_engine.utils.empty_protected_read(anki_engine.Label, label_id)
    bot.edit_message_text(
        str(label),
        call.message.chat.id, call.message.id,
        reply_markup=keyboards.get_base_label_inline(label_id)
    )


def show_label(
        chat_id: int, bot: telebot.TeleBot, label: anki_engine.Label,
        markup_function=keyboards.get_base_label_inline
):
    return bot.send_message(
        chat_id, str(label),
        reply_markup=markup_function(label.id)
    )


def show_user_labels(
        chat_id: int, user_id: int, bot: telebot.TeleBot,
        markup_function=keyboards.get_base_label_inline, filter_function=lambda label: True
):
    labels = list(filter(filter_function, anki_engine.get_user_labels(user_id)))
    for label in labels:
        show_label(chat_id, bot, label, markup_function)
    if len(labels) == 0:
        bot.send_message(chat_id, messages.EMPTY_LABELS_LIST)


def show_edit_inline(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    label_id = int(call.data.split(' ')[1])
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.id,
        reply_markup=keyboards.get_edit_label_inline(label_id)
    )


def switch_label_permission(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    user_id = call.from_user.id
    label_id = int(call.data.split(' ')[1])
    label = anki_engine.label_controls.switch_permission(user_id, label_id)
    bot.edit_message_text(
        str(label), call.message.chat.id, call.message.id,
        reply_markup=keyboards.get_base_label_inline(label_id)
    )


def ask_new_label_name(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    label_id = int(call.data.split(' ')[1])
    new_message = utils.send_message_with_force_reply_placeholder(
        bot, call.message.chat.id, messages.EDIT_LABEL_NAME_PLACEHOLDER,
        messages.EDIT_LABEL_NAME_MESSAGE,
        reply_to_message_id=call.message.id
    )
    bot.register_for_reply(new_message, edit_label_name, bot, label_id)


def edit_label_name(message: telebot.types.Message, bot: telebot.TeleBot, label_id):
    label = anki_engine.label_controls.update(message.from_user.id, label_id, message.text)
    label.save()
    bot.send_message(
        message.chat.id, messages.EDIT_LABEL_NAME_SUCCESS,
        reply_markup=base_keyboards.get_base_markup()
    )
    show_label(message.chat.id, bot, label)


def proof_deletion(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    label_id = int(call.data.split(' ')[1])
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.id,
        reply_markup=keyboards.get_delete_label_inline(label_id)
    )


def delete_label(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    bot.delete_message(call.message.chat.id, call.message.id)
    label_id = int(call.data.split(' ')[1])
    anki_engine.label_controls.delete(call.from_user.id, label_id)
