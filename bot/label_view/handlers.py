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


def get_private_flag(message: telebot.types.Message, bot: telebot.TeleBot):
    bot.send_message(
        message.chat.id, 'Сделать доступной тренировку по этому заголовку всем желающим '
                         '(без возможности какого-либо редактирования)',
        reply_markup=keyboards.get_yes_no_inline()
    )


def ask_label_name(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    placeholder = telebot.types.ForceReply(
        input_field_placeholder=f'Название заголовка'
    )
    new_message = bot.send_message(
        call.message.chat.id, 'Введите название заголовка ответом на это сообщение',
        reply_markup=placeholder
    )
    is_private = 'private' in call.data
    # bot.register_next_step_handler(new_message, create_label, bot, is_private)
    bot.register_for_reply(new_message, create_label, bot, is_private)


def create_label(message: telebot.types.Message, bot: telebot.TeleBot, is_private: bool):
    label = anki_engine.label_controls.create(message.from_user.id, message.text, is_private)
    bot.send_message(
        message.chat.id, 'Заголовок успешно создан',
        reply_markup=base_keyboards.get_base_markup()
    )
    show_label(message.chat.id, bot, label)


def set_base_label_menu(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    label_id = int(call.data.split(' ')[1])
    bot.edit_message_reply_markup(
        call.message.chat.id, call.message.id,
        reply_markup=keyboards.get_base_label_inline(label_id)
    )


def show_label(chat_id: int, bot: telebot.TeleBot, label: anki_engine.Label):
    bot.send_message(
        chat_id, str(label),
        reply_markup=keyboards.get_base_label_inline(label.id)
    )


def show_user_labels(message: telebot.types.Message, bot: telebot.TeleBot):
    labels = anki_engine.get_user_labels(message.from_user.id)
    for label in labels:
        show_label(message.chat.id, bot, label)
    if len(labels) == 0:
        bot.send_message(message.chat.id, 'У вас пока нет заголовков. Создайте новый!')


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
    placeholder = telebot.types.ForceReply(
        input_field_placeholder=f'Новое название заголовка'
    )
    new_message = bot.send_message(
        call.message.chat.id, reply_markup=placeholder, reply_to_message_id=call.message.id,
        text=f'Введите новое название заголовка ответом на это сообщение (Работает один раз)',

    )
    bot.register_for_reply(new_message, edit_label_name, bot, label_id)


def edit_label_name(message: telebot.types.Message, bot: telebot.TeleBot, label_id):
    label = anki_engine.label_controls.update(message.from_user.id, label_id, message.text)
    label.save()
    bot.send_message(
        message.chat.id, 'Название заголовка изменено',
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
    bot.answer_callback_query(call.id, 'Заголовок успешно удалён')
