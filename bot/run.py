import logging
import os
import telebot

from config import TOKEN

import bot.base_view.handlers as base_view
import bot.card_view.handlers as card_view
import bot.label_view.handlers as label_view
import bot.relations_view.handlers as relations_view
import bot.train_view.handlers as train_view

import bot.base_view.messages as base_messages

os.path.join('..')


def start():
    bot = telebot.TeleBot(TOKEN)

    base_view.bind_handlers(bot)
    card_view.bind_handlers(bot)
    label_view.bind_handlers(bot)
    relations_view.bind_handlers(bot)
    train_view.bind_handlers(bot)

    # requests logging
    logging.basicConfig(filename='filename.log', level=logging.DEBUG,
                        format=' %(asctime)s - %(levelname)s - %(message)s')
    # bot logging
    telebot.logger.setLevel('DEBUG')

    bot.infinity_polling()


if __name__ == '__main__':
    start()
