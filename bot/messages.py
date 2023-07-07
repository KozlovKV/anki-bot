from enum import Enum, StrEnum
import telebot


WELCOME = """\
Привет, я помогу тебе запоминать любую информацию. 

Просто добавь карточки, создай для них заголовок, свяжи их между собой и начинай тренировку.

В зависимости от того, насколько хорошо ты помнишь содержание карточки, поставь оценку. 
Она повлияет на то, через сколько я спрошу карточку повторно"""


class BaseButtonsEnum(Enum):
    ADD_CARD = 0
    ADD_LABEL = 1
    SHOW_CARDS = 2
    SHOW_LABELS = 3
    ADD_RELATION = 4
    TRAIN = 5


BASE_BUTTONS = [
    'Добавить карточку',
    'Добавить заголовок',
    'Посмотреть мои карточки',
    'Посмотреть мои заголовки',
    'Связать карточку с заголовком',
    'Тренироваться'
]


def get_base_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*BASE_BUTTONS)
    return markup


def get_yes_no_markup():
    return telebot.types.ReplyKeyboardMarkup().add('Да', 'Нет')


def get_count_markup():
    return telebot.types.ReplyKeyboardMarkup(row_width=4).add('5', '10', '25', '50')


def get_quality_markup():
    return telebot.types.ReplyKeyboardMarkup(row_width=6).add('0', '1', '2', '3', '4', '5')
