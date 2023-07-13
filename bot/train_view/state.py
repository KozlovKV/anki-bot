import telebot


class TrainState(telebot.handler_backends.StatesGroup):
    train_list_length = telebot.handler_backends.State()
    train_list = telebot.handler_backends.State()
