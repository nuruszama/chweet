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

CHOOSING, TYPING_CHOICE, TYPING_REPLY = range (3)

def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f'{key} - {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        "Hi! I am Sweety, the cutest 🐈 in the world."
        "About what you would like to talk to me"
        "eg: Name, age, hobbies. Reply anything like this"
    )
    Return CHOOSING

def name(update, context):
    update.message.reply_text(
       "Oh 😬 I haven't asked you your name yet!"
       "What is your name? 😀"
       )

    return TYPING_REPLY

def hello(update, context):
    update.message.reply_text(
       "Hey, How are you? 🤠"
       )

    return TYPING_REPLY

def nice(update, context):
    update.message.reply_text(
       "Nice to hear that 🤗"
       "Is there anything else"
       )

    return TYPING_REPLY

def regular_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(f'Your {text.lower()}? Yes, I would love to hear about that!')

    return TYPING_REPLY

def custom_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for a description of a custom category."""
    update.message.reply_text(
        "Alright, please send me the category about which you wish to talk"
        "for example 'Most impressive skill'"
        )

    return TYPING_CHOICE

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        "Help! I'm happy to assist you."
        "But right now, I'm still learning"
        )

def received_information(update: Update, context: CallbackContext) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)} You can tell me more, or change your opinion"
        " on something.",
        reply_markup=markup,
    )

    return CHOOSING

def done(update: Update, context: CallbackContext) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
        f"I learned these facts about you: {facts_to_str(user_data)}Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END

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

def done(update: Update, context: CallbackContext) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
        f"I learned these facts about you: {facts_to_str(user_data)}Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END

    # on noncommand i.e message - welcome message,
    # echo the message, end message on Telegram
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Hi@chweetbot)$'), start)],
        states={
            CHOOSING: [
                MessageHandler(Filters.regex('^(Name)$'), name),
                MessageHandler(Filters.regex('^(Hi|Hello|Hola|Hey|Oii)$'), Hello),
                MessageHandler(Filters.regex('^(Fine)$'), nice),
                MessageHandler(Filters.regex('^Something else...$'), custom_choice),
            ],
            TYPING_CHOICE: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                    regular_choice)
            ],
            TYPING_REPLY: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                    received_information),
            ],
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    TOKEN = '1871713199:AAErm5PtO90eUeROUf0IN6DcNnLgRvxpDNc'
    LINK = 'https://chweety.herokuapp.com/'
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(LINK + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
