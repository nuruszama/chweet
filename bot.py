 """Simple bot that can foward your messages to your group.
 I'm not an expert, so if anyone can simplify this codes,
 suugestions are welcomed"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
import os
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Some of secret code will be hidden from others who view our code.
# So we need to declare that secrets here using os.envriron['_']
TOKEN = os.environ['TOKEN']
owner= os.environ['OWNER']
pic= os.environ['Pro_Pic']
dumb= os.environ['Dumbing_Group']
channel= os.environ['Channel']
mail_id= os.environ['Mail_id']
url= os.environ['webhook_url']

# Create the Updater and pass it your bot's token.
# Make sure to set use_context=True to use the new context based callbacks
# Post version 12 this will no longer be necessary
updater = Updater(TOKEN, use_context=True)
dp_add = updater.dispatcher.add_handler

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

#Send a message when the command /start is issued.
def start(update, context) -> None:
    user = update.message.from_user
    firstname = "{}".format(user['first_name'])
    lastname = "{}".format(user['last_name'])
    username = "{}".format(user['username'])
    if lastname == "None":
        if username == "None":
            fullname = "{}".format(user['first_name'])
        else:
            fullname = "{} [ @{} ]".format(user['first_name'],user['username'])
    else:
        if username == "None":
            fullname = "{} {}".format(user['first_name'],user['last_name'])
        else:
            fullname = "{} {} [ @{} ]".format(user['first_name'],user['last_name'],user['username'])
    context.bot.send_photo(chat_id=update.message.chat_id, photo = pic, caption=
        f"Hi {fullname} 🙂 I'm Sweety, cutest 🐈 in telegram")
    context.bot.send_message(chat_id=update.message.chat_id, text=
        f"Feel free to send a mail at {mail_id} if you have any doubts")
    context.bot.send_message(chat_id=dumb, text=f"{fullname} started conversation with me")
dp_add(CommandHandler("start", start))
   
def doc(update, context):
    user = update.message.from_user
    firstname = "{}".format(user['first_name'])
    lastname = "{}".format(user['last_name'])
    username = "{}".format(user['username'])
    if lastname == "None":
        if username == "None":
            fullname = "{}".format(user['first_name'])
        else:
            fullname = "{} [ @{} ]".format(user['first_name'],user['username'])
    else:
        if username == "None":
            fullname = "{} {}".format(user['first_name'],user['last_name'])
        else:
            fullname = "{} {} [ @{} ]".format(user['first_name'],user['last_name'],user['username'])
    file_name = update.message.document.file_name
    chatid = update.message.chat_id
    if update.message.chat_id==owner:
        if update.message.forward_from_chat.id==channel:
            context.bot.send_document(chat_id=owner, document=update.message.document.file_id, caption=update.message.caption)
        else:
            context.bot.send_document(chat_id=channel, document=update.message.document.file_id, caption=update.message.caption)
        context.bot.delete_message(message_id=update.message.message_id, chat_id=owner)
    else:
        if update.message.forward_from_chat.id==channel:
            context.bot.send_document(chat_id=chatid, document=update.message.document.file_id, caption=update.message.caption)
        else:
            context.bot.send_document(chat_id=chatid, document=update.message.document.file_id, caption=update.message.caption)
            context.bot.send_document(chat_id=channel, document=update.message.document.file_id, caption=update.message.caption)
            context.bot.send_message(chat_id=dumb, text=f"Added {file_name} from {fullname}")
        context.bot.delete_message(message_id=update.message.message_id, chat_id=chatid)
dp_add(MessageHandler(Filters.document, doc))

def vid(update, context):
    user = update.message.from_user
    firstname = "{}".format(user['first_name'])
    lastname = "{}".format(user['last_name'])
    username = "{}".format(user['username'])
    if lastname == "None":
        if username == "None":
            fullname = "{}".format(user['first_name'])
        else:
            fullname = "{} [ @{} ]".format(user['first_name'],user['username'])
    else:
        if username == "None":
            fullname = "{} {}".format(user['first_name'],user['last_name'])
        else:
            fullname = "{} {} [ @{} ]".format(user['first_name'],user['last_name'],user['username'])
    file_name = update.message.caption
    chatid = update.message.chat_id
    if update.message.chat_id==owner:
        if update.message.forward_from_chat.id==channel:
            context.bot.send_video(chat_id=owner, video=update.message.video.file_id, caption=update.message.caption)
        else:
            context.bot.send_video(chat_id=channel, video=update.message.video.file_id, caption=update.message.caption)
        context.bot.delete_message(message_id=update.message.message_id, chat_id=owner)
    else:
        if update.message.forward_from_chat.id==channel:
            context.bot.send_video(chat_id=chatid, video=update.message.video.file_id, caption=update.message.caption)
        else:
            context.bot.send_video(chat_id=chatid, video=update.message.video.file_id, caption=update.message.caption)
            context.bot.send_video(chat_id=channel, video=update.message.video.file_id, caption=update.message.caption)
            context.bot.send_message(chat_id=dumb, text=f"Added {file_name} from {fullname}")
        context.bot.delete_message(message_id=update.message.message_id, chat_id=chatid)
dp_add(MessageHandler(Filters.video, vid))

#Log Errors caused by Updates.
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
updater.dispatcher.add_error_handler(error)

#Start the bot.
def main():
    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(url + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
