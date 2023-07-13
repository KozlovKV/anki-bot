import logging
import telebot
import sys

from .config import TOKEN

from .base_view import handlers as base_view
from .card_view import handlers as card_view
from .label_view import handlers as label_view
# from .relations_view import handlers as relations_view
# from .train_view import handlers as train_view


def start():
    bot = telebot.TeleBot(TOKEN)

    base_view.bind_handlers(bot)
    card_view.bind_handlers(bot)
    label_view.bind_handlers(bot)
    # relations_view.bind_handlers(bot)
    # train_view.bind_handlers(bot)

    # requests logging
    logging.basicConfig(filename='log/api.log', level=logging.DEBUG,
                        format=' %(asctime)s - %(levelname)s - %(message)s')
    # bot logging
    sys.stdout = open('./log/bot_main.log', 'w')
    sys.stderr = open('./log/bot_error.log', 'w')
    if '--debug' in sys.argv:
        telebot.logger.setLevel('DEBUG')

    bot.enable_saving_states()

    bot.infinity_polling()


if __name__ == '__main__':
    start()
