#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import subprocess
import configparser
import logging
import strings

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

config = configparser.ConfigParser()
config.read("properties.ini")

updater = Updater(config["KEY"]["tg_API_token"])


global owner_ID
owner_ID = int(config["ADMIN"]["admin_ID"])

global Alexandra_ID
alexandra_ID = int(config["SECRET"]["Alexandra_ID"])


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def start(bot, update):
	update.message.reply_text(strings.stringHelp)

def unknown(bot, update):
	update.message.reply_text(strings.errorUnknownCommand)

def help(bot, update):
	update.message.reply_text(text=help_all)


def ip(bot, update):
    sender = update.message.from_user

    if sender.id == owner_ID:
        try:
            update.message.reply_text("Server IP: " + subprocess.check_output(["curl", "ipinfo.io/ip"], universal_newlines=True, timeout=5))
        except CalledProcessError: update.message.reply_text(strings.errorMessage)
        except TimeoutExpired: update.message.reply_text(strings.errorTimeout)
    else:
        update.message.reply_text(strings.stringAdminOnly)


def getid(bot, update):
	sender = update.message.from_user

	sender_id = str(sender.id)

	update.message.reply_text(sender.username + "'s ID is " + sender_id)


def alexandra(bot, update):
    sender = update.message.from_user

    if sender.id == alexandra_ID:
        supdate.message.reply_text(strings.stringAlexandra)
    else:
        update.message.reply_text(strings.errorAlexandra)


help_all = strings.help_message + strings.help_ip + strings.help_id


dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("ip", ip))
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_handler(CommandHandler("id", getid))
dispatcher.add_handler(CommandHandler("alexandra", alexandra))

dispatcher.add_handler(MessageHandler(Filters.command, unknown))

updater.start_polling()
updater.idle()
