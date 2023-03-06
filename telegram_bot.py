import logging
import os
import telegram

from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)
from dialog_flow import detect_intent_texts


logger = logging.getLogger(__name__)


class MyLogsHandler(logging.Handler):
    """Logger handler for Telegram"""

    def __init__(self, bot, tg_token, tg_chat_id):

        super().__init__()
        self.bot = bot
        self.tg_token = tg_token
        self.tg_chat_id = tg_chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.tg_chat_id, text=log_entry)


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def send_message(update: Update, context: CallbackContext):
    """Echo the user message."""
    if detect_intent_texts(update.message.text) != '<is_fallback>':
        update.message.reply_text(detect_intent_texts(update.message.text))


def main():
    load_dotenv()
    tg_token = os.getenv('TELEGRAM_TOKEN')
    tg_debug_token = os.getenv('TELEGRAM_DEBUG_TOKEN')
    tg_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    tg_debug_bot = telegram.Bot(token=tg_debug_token)

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_message))  # noqa

    logger.setLevel(level=logging.INFO)
    logger.addHandler(MyLogsHandler(tg_debug_bot, tg_debug_token, tg_chat_id))
    logger.info('Telegram-bot is Run!')

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
