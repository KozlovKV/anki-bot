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
    bot.register_callback_query_handler(
        delete_card,
        func=lambda call: '/card/delete/proof' in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        proof_deletion,
        func=lambda call: '/card/delete ' in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        delete_card,
        func=lambda call: '/card/delete/proof ' in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        ask_edit_side,
        func=lambda call: '/card/edit ' in call.data,
        pass_bot=True
    )
    bot.register_callback_query_handler(
        ask_new_side_text,
        func=lambda call: '/card/edit/' in call.data,
        pass_bot=True
    )


def get_first_card_side(message, bot: telebot.TeleBot):
    new_message = bot.send_message(message.chat.id, 'Введите первую сторону карточки')
    bot.register_next_step_handler(new_message, get_second_card_side, bot)


def get_second_card_side(message, bot: telebot.TeleBot):
    new_message = bot.send_message(message.chat.id, 'Введите вторую сторону карточки')
    bot.register_next_step_handler(new_message, create_card, bot, message.text)


def create_card(message, bot: telebot.TeleBot, side1: str):
    new_message = bot.send_message(
        message.chat.id, 'Карточка успешно создана',
        reply_markup=messages.get_base_markup()
    )
    card = anki_engine.card_controls.create(message.from_user.id, side1, message.text)
    show_card(new_message, bot, card)


# TODO: Вынести щаблоны для инлайнов в константы, чтобы не допустить ошибок с проверкой
def show_card(message, bot: telebot.TeleBot, card: anki_engine.Card):
    inline = telebot.util.quick_markup({
        'Связать с заголовком': {'callback_data': f'/card/relation/create {card.id}'},
        'Изменить': {'callback_data': f'/card/edit {card.id}'},
        'Удалить': {'callback_data': f'/card/delete {card.id}'},
    }, row_width=5)
    bot.send_message(
        message.chat.id, card.str_with_labels(),
        reply_markup=inline
    )


def show_user_cards(message, bot: telebot.TeleBot):
    cards = anki_engine.get_user_cards(message.from_user.id)
    for card in cards:
        show_card(message, bot, card)
    if len(cards) == 0:
        bot.send_message(message.chat.id, 'У вас пока нет карточек. Скорее создайте первую!')


def ask_edit_side(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    card_id = int(call.data.split(' ')[1])
    inline = telebot.util.quick_markup({
        'Изменить первую сторону': {'callback_data': f'/card/edit/1 {card_id}'},
        'Изменить вторую сторону': {'callback_data': f'/card/edit/2 {card_id}'},
    }, row_width=2)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=inline)


def ask_new_side_text(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    data = call.data.split(' ')
    side_number = int(data[0].split('/')[-1])
    card_id = int(data[1])
    new_message = bot.send_message(call.message.chat.id, f'Введите новый текст стороны {side_number}')
    bot.register_next_step_handler(new_message, edit_side, bot, side_number, card_id)


def edit_side(message: telebot.types.Message, bot: telebot.TeleBot, side_number, card_id):
    card = anki_engine.utils.user_protected_read(anki_engine.Card, message.from_user.id, card_id)
    if side_number == 1:
        card.side1 = message.text
    else:
        card.side2 = message.text
    card.save()
    new_message = bot.send_message(
        message.chat.id, 'Карточка успешно изменена',
        reply_markup=messages.get_base_markup()
    )
    show_card(new_message, bot, card)


def proof_deletion(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    card_id = int(call.data.split(' ')[1])
    inline = telebot.util.quick_markup({
        'Подтвердить удаление': {'callback_data': f'/card/delete/proof {card_id}'},  # TODO: Добавить обратную кнопку
    }, row_width=1)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=inline)


def delete_card(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    bot.delete_message(call.message.chat.id, call.message.id)
    card_id = int(call.data.split(' ')[1])
    anki_engine.card_controls.delete(call.from_user.id, card_id)
    bot.answer_callback_query(call.id, 'Карточка успешно удалена')
