import telebot

from secret import TOKEN

import messages
import card_view
import label_view
import relations_view
import train_view


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, messages.WELCOME, reply_markup=messages.get_base_markup())


@bot.message_handler(commands=['keyboard'])
def show_menu(message):
    bot.send_message(message.chat.id, 'Доступные действия', reply_markup=messages.get_base_markup())


def start():
    card_view.bind_handlers(bot)
    label_view.bind_handlers(bot)
    relations_view.bind_handlers(bot)
    train_view.bind_handlers(bot)

    bot.set_my_commands(messages.get_commands_list(), language_code='ru')

    bot.infinity_polling()


if __name__ == '__main__':
    start()
