"""
Simple Bot to reply to Telegram messages taken from the python-telegram-bot examples.
Deployed using heroku.
"""

import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

import os
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '1871713199:AAErm5PtO90eUeROUf0IN6DcNnLgRvxpDNc'
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! I am Sweety, the cutest 🐈 in the world. Happy to meet you')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help! I am happy to assist you. Right now, I am still learning')

def end(update, context):
    update.message.reply_text('Happy that you send me a message 😀 I cannot completely text you back. I am still learning')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

    return END

def incoming(update, context):
    update.message.reply_text('Hi, you send me')

    return ECHO

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

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, incoming)],
        states={
                ECHO: [
                MessageHandler(
                     (MessageHandler(Filters.text, echo)
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.text, end)],
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://chweety.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
