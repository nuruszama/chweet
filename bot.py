"""
Simple Bot to resend to Telegram videos or documents inspired from the python-telegram-bot examples.
Deployed using heroku.
"""

import logging

from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

import os
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '1871713199:AAGEn6U4aD2u0EGlwxsXJmbgTsey-cKoimI'


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        "Hi @#{message.from.username}! I am Sweety, the cutest 🐈 in the world.")
    update.message.reply_text(
        "I will assist you to send documents and videos without forward tag")

def docs(update, context):
    """fetching file_id and resending to destination"""
    If update.message.
    context.bot.send_document(chat_id=update.message.chat_id,
                               document=update.message.file_id)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(**, docs))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    """replace link with the link to your app"""
    updater.bot.setWebhook('chweety.herokuapp.com' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
