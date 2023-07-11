from enum import Enum
import telebot


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class BaseButtonsEnum(ExtendedEnum):
    ADD_CARD = 'Добавить карточку'
    ADD_LABEL = 'Добавить заголовок'
    SHOW_CARDS = 'Мои карточки'
    SHOW_LABELS = 'Мои заголовки'
    TRAIN = 'Тренироваться'


def get_base_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*BaseButtonsEnum.list())
    return markup

