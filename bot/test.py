import telebot

from secret import TOKEN
import messages

from core import anki_engine

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, messages.WELCOME, reply_markup=messages.get_base_markup())


@bot.message_handler(regexp=messages.BASE_BUTTONS[0])  # TODO: нормальный вариант без индексов
def get_first_card_side(message):
    new_message = bot.send_message(message.chat.id, 'Введите первую сторону карточки')
    bot.register_next_step_handler(new_message, get_second_card_side)


def get_second_card_side(message):
    new_message = bot.send_message(message.chat.id, 'Введите вторую сторону карточки')
    bot.register_next_step_handler(new_message, create_card, message.text)


def create_card(message, side1):
    card = anki_engine.card.create(message.from_user.id, side1, message.text)
    bot.send_message(message.chat.id, 'Карточка успешно создана')


@bot.message_handler(func=lambda: True)
def show_menu(message):
    bot.send_message(message.chat.id, 'Доступные действия', reply_markup=messages.get_base_markup())


bot.infinity_polling()
