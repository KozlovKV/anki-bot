from enum import Enum
import telebot


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class BaseButtonsEnum(ExtendedEnum):
    ADD_CARD = 'Добавить карточку'
    ADD_LABEL = 'Добавить заголовок'
    SHOW_CARDS = 'Посмотреть мои карточки'
    SHOW_LABELS = 'Посмотреть мои заголовки'
    ADD_RELATION = 'Связать карточку с заголовком'
    TRAIN = 'Тренироваться'


def get_base_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*BaseButtonsEnum.list())
    return markup


def get_count_markup():
    return telebot.types.ReplyKeyboardMarkup(row_width=4).add('5', '10', '25', '50')


def get_quality_markup():
    return telebot.types.ReplyKeyboardMarkup(row_width=6).add('0', '1', '2', '3', '4', '5')

