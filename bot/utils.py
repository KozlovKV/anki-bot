import telebot


def delete_message_by_handling(
        new_message: telebot.types.Message, bot: telebot.TeleBot,
        message_for_deleting: telebot.types.Message, timeout=5
):
    bot.delete_message(message_for_deleting.chat.id, message_for_deleting.id, timeout)
