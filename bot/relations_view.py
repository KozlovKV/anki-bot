import telebot

import messages

from core import anki_engine


def bind_handlers(bot: telebot.TeleBot):
    bot.register_message_handler(
        ask_card_id,
        regexp=messages.BASE_BUTTONS[messages.BaseButtonsEnum.ADD_RELATION.value],
        pass_bot=True
    )
    bot.register_message_handler(
        create_relation_from_command,
        commands=['chain'],
        pass_bot=True
    )


def ask_card_id(message, bot: telebot.TeleBot):
    new_message = bot.send_message(message.chat.id, 'Введите ID карточки')
    bot.register_next_step_handler(new_message, handle_card_id, bot)


# TODO: Добавить валидацию по правам доступа, наличию номера и корректности ввода (число)
def handle_card_id(message, bot: telebot.TeleBot):
    card_id = int(message.text)
    new_message = bot.send_message(message.chat.id, 'Введите ID заголовка')
    bot.register_next_step_handler(new_message, handle_label_id, bot, card_id)


# TODO: Добавить валидацию по правам доступа, наличию номера и корректности ввода (число)
def handle_label_id(message, bot: telebot.TeleBot, card_id: int):
    label_id = int(message.text)
    create_relation(message, bot, card_id, label_id)


def create_relation(message, bot: telebot.TeleBot, card_id: int, label_id: int):
    card = anki_engine.utils.user_protected_read(anki_engine.Card, message.from_user.id, card_id)
    label = anki_engine.utils.user_protected_read(anki_engine.Label, message.from_user.id, label_id)
    relation = anki_engine.relation_controls.create_by_instances(message.from_user.id, card, label)
    text = f'Карточка\n\n {card}\n\nУспешно связана с заголовком\n\n {label}' \
        if relation[1] else \
        f'Связь между карточкой\n\n {card}\nИ заголовком\n\n {label}\n\nуже есть'
    bot.send_message(
        message.chat.id, text, reply_markup=messages.get_base_markup()
    )


def create_relation_from_command(message, bot: telebot.TeleBot):
    args = message.text.strip().split(' ')
    card_id = int(args[1])
    label_id = int(args[2])
    create_relation(message, bot, card_id, label_id)
