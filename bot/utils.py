from typing import Optional

import telebot


def check_int(value: any):
    try:
        int_number = int(value)
    except ValueError:
        return None
    return int_number


def delete_message_by_handling(
        new_message: telebot.types.Message, bot: telebot.TeleBot,
        message_for_deleting: telebot.types.Message, timeout=5
):
    bot.delete_message(message_for_deleting.chat.id, message_for_deleting.id, timeout)


def send_message_with_force_reply_placeholder(
        bot: telebot.TeleBot, chat_id: int, placeholder_text: str, new_message_text: str,
        reply_to_message_id: Optional[int] = None, **kwargs
) -> telebot.types.Message:
    placeholder = telebot.types.ForceReply(input_field_placeholder=placeholder_text)
    return bot.send_message(
        chat_id, new_message_text, reply_markup=placeholder,
        reply_to_message_id=reply_to_message_id, **kwargs
    )


def get_kwargs_for_message_with_force_reply_placeholder(
        chat_id: int, placeholder_text: str, new_message_text: str,
        reply_to_message_id: Optional[int] = None, **kwargs
):
    placeholder = telebot.types.ForceReply(input_field_placeholder=placeholder_text)
    return {
        'chat_id': chat_id,
        'text': new_message_text,
        'reply_markup': placeholder,
        'reply_to_message_id': reply_to_message_id,
        **kwargs
    }
