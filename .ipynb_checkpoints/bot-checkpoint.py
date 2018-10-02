import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler


token = "579014326:AAH2oxwrQug6pV_lgTPIeIGyRTe9XMAMqXk"
chat_id = "67923752"


def start(bot, update):
    greeting_text = "Hi {}\nYour updates will be shown here".format(update.message.from_user.first_name)
    print(greeting_text)
    print(update.message.chat_id)
    bot.send_message(chat_id=update.message.chat_id, text=greeting_text)

def send_update(text=""):
    le_bot.send_message(chat_id=chat_id, text=text)


def main():
    global le_bot
    le_bot = telegram.Bot(token)
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()

    
if __name__ == "__main__":
    main()