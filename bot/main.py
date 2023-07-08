import os
import telebot

from secret import TOKEN

import messages
import keyboards

import bot.card_view.handlers as card_view
import bot.label_view.handlers as label_view
import bot.relations_view.handlers as relations_view
import bot.train_view.handlers as train_view


os.path.join('..')


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, messages.WELCOME, reply_markup=keyboards.get_base_markup())


@bot.message_handler(commands=['keyboard'])
def show_menu(message):
    bot.send_message(message.chat.id, 'Доступные действия', reply_markup=keyboards.get_base_markup())


def start():
    card_view.bind_handlers(bot)
    label_view.bind_handlers(bot)
    relations_view.bind_handlers(bot)
    train_view.bind_handlers(bot)

    bot.set_my_commands(messages.get_commands_list(), language_code='ru')

    bot.infinity_polling()


if __name__ == '__main__':
    start()
