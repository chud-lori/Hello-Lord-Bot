"""
Bot system
"""

import os
import random
import logging
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8443'))
APP_NAME = # BOT HOST
TOKEN = # BOT TOKEN

# randomize cat images
rana = [i for i in range(120, 5000)] # pylint: disable=unnecessary-comprehension
ranb = [i for i in range(120, 5000)] # pylint: disable=unnecessary-comprehension

def start(update, context): # pylint: disable=unused-argument
    """Send a message when the command /start is issued."""
    update.message.reply_text('''
    Hi!
    This bot was developed by Lori
    type /help to see how use it
    Enjoy the Lord's images
    ''')


def help(update, context): # pylint: disable=unused-argument, redefined-builtin
    """Send a message when the command /help is issued."""
    update.message.reply_text("""
    Type: 
        /lord to see lord's images
        /woof to see woof's images
        /advice to get advice from Lord
    """)


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(context)
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def woof_get_url():
    """Get image from random.dog."""
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def woof(update, context):
    """Send a random dog images."""
    url = woof_get_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)

def lord(update, context):
    """Send a random cat images."""
    url = 'https://placekitten.com/g/{}/{}'.format(random.choice(rana), random.choice(ranb))
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)

def advice(update, context):
    """Send a random advice"""
    url = requests.get('https://api.adviceslip.com/advice').json()
    advice = url['slip']['advice']
    send = f"""
    Lord's advice:
    {advice}
    """
    update.message.reply_text(send)


# def main():
#     updater = Updater()
#     dp = updater.dispatcher
#     dp.add_handler(CommandHandler('lord',lord))
#     updater.start_polling()
#     updater.idle()

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher # pylint: disable=invalid-name

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("lord", lord))
    dp.add_handler(CommandHandler("woof", woof))
    dp.add_handler(CommandHandler("advice", advice))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    # updater.bot.set_webhook(url=settings.WEBHOOK_URL)
    updater.bot.set_webhook(APP_NAME + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
