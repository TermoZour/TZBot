#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler
import subprocess
import configparser
import logging
import strings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

config = configparser.ConfigParser()
config.read("properties.ini")

updater = Updater(config["KEY"]["tg_API_token"])


global owner_ID
owner_ID = int(config["ADMIN"]["admin_ID"])


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def ip(bot, update):
    sender = update.message.from_user

    if sender.id == owner_ID:
        try:
            update.message.reply_text("Server IP: " + subprocess.check_output(["curl", "ipinfo.io/ip"], universal_newlines=True, timeout=5))
        except CalledProcessError: update.message.reply_text(strings.errorMessage)
        except TimeoutExpired: update.message.reply_text(strings.errorTimeout)
    else:
        update.message.reply_text(strings.stringAdminOnly)



def start(bot, update):
	update.message.reply_text(strings.stringHelp)


def unknown(bot, update):
	update.message.reply_text(strings.errorUnknownCommand)


def help(bot, update):
	update.message.reply_text(text=help_all)


def getid(bot, update):
	sender = update.message.from_user

	sender_id = str(sender.id)

	update.message.reply_text(sender.username + "'s ID is " + sender_id)


def alexandra(bot, update):
 update.message.reply_text(strings.stringAlexandra)


help_all = strings.help_message + strings.help_ip + strings.help_id


dispatcher = updater.dispatcher

ip_handler = CommandHandler("ip", ip)
dispatcher.add_handler(ip_handler)

start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

unknown_handler = CommandHandler("unknown", unknown)
dispatcher.add_handler(unknown_handler)

help_handler = CommandHandler("help", help)
dispatcher.add_handler(help_handler)

tg_id_handler = CommandHandler("id", getid)
dispatcher.add_handler(tg_id_handler)

alexandra_handler = CommandHandler("alexandra", alexandra)
dispatcher.add_handler(alexandra_handler)


updater.start_polling()
updater.idle()
