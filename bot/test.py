import telebot

from secret import TOKEN
import messages

from core.anki_engine import AnkiSession

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, messages.WELCOME, reply_markup=messages.get_base_markup())


@bot.message_handler(regexp=messages.BASE_BUTTONS[0])  # TODO: нормальный вариант без индексов
def create_card_prefix(message):
    new_message = bot.send_message(message.chat.id, 'Введите обе стороны карточки через слэш')
    bot.register_next_step_handler(new_message, create_card)


def create_card(message):
    s = AnkiSession(message.from_user.id)
    s.create_card(message.text)
    new_message = bot.send_message(message.chat.id, 'Карточка успешно создана')
    bot.register_next_step_handler(new_message, show_menu)


@bot.message_handler(func=lambda: True)
def show_menu(message):
    bot.send_message(message.chat.id, 'Доступные действия', reply_markup=messages.get_base_markup())


bot.infinity_polling()
