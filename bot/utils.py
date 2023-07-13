from typing import Optional

import telebot


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


def edit_message_with_force_reply_placeholder(
        bot: telebot.TeleBot, chat_id: int, message_id: int,
        placeholder_text: str, new_message_text: str, **kwargs
) -> telebot.types.Message:
    placeholder = telebot.types.ForceReply(input_field_placeholder=placeholder_text)
    return bot.edit_message_text(
        new_message_text, chat_id, message_id, reply_markup=placeholder, **kwargs
    )
