import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler

import json


class MonitorBot(object):

    def __init__(self, token):
        self.bot = telegram.Bot(token=token)
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        # Will be set during first messages. The bot is intended for single user
        self.chat_id = None
        self.last_message_id = None

    def start(self):
        start_handler = CommandHandler('start', self.greeting)
        self.dispatcher.add_handler(start_handler)
        self.updater.start_polling()

    def greeting(self, bot, update):
        self.chat_id = update.message.chat_id
        greeting_text = "Hi {}\nYour updates will be shown here".format(update.message.from_user.first_name)
        greeting_text += "\nYour chat id is {}".format(self.chat_id)
        self.bot.send_message(chat_id=self.chat_id, text=greeting_text)

    def compose_message(self, logs):
        message = ""
        for k, v in logs.items():
            message += str(k).title() + " : " + str(v) + "\n"
        
        return message

    def send_update(self, logs):
        message = self.compose_message(logs)
        print(message)
        if "batch" in logs:
            if self.last_message_id == None or logs['batch'] == 0:
                sent_msg = self.bot.send_message(chat_id=self.chat_id, text=message)
                self.last_message_id = sent_msg.message_id
            else:
                self.bot.edit_message_text(chat_id=self.chat_id, message_id=self.last_message_id, text=message)
        else:
            self.bot.send_message(chat_id=self.chat_id, text=message)
            self.last_message_id = None

