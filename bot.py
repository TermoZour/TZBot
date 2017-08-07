#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from telegram.ext.dispatcher import run_async

import subprocess
import requests
import ConfigParser
import logging
import strings
import os
import json
import time
import sys


config = ConfigParser.ConfigParser()
config.read("properties.ini")

loc_notesjson = "./data/notes.json"
loc_restart_id = "./data/id_file.json"

owner_id = int(config.get("ADMIN", "admin_id"))

def loadjson(path):
    if not os.path.isfile(path) or not os.access(path, os.R_OK):
        name = {}
        dumpjson(path, name)
    with open(path) as f:
        name = json.load(f)
    return name


def dumpjson(filename, var):
    with open(filename, "w") as file:
        json.dump(var, file)


def start(bot, update):
    update.effective_message.reply_text(strings.stringHelp)


def unknown(bot, update):
    update.effective_message.reply_text(strings.errorUnknownCommand)


def help(bot, update):
    update.effective_message.reply_text(text=help_all)


def test(bot, update):
    update.effective_message.reply_text("Bot status: Online, duh")

def restart(bot, update):
    sender = update.message.from_user

    chat_id = str(update.message.chat_id)

    if sender.id == owner_id:
        with open(loc_restart_id, "w") as f:
            f.write(chat_id)

        update.effective_message.reply_text("Bot is restarting...")
        time.sleep(0.5)
        os.execl(sys.executable, sys.executable, *sys.argv)
        #os.execv(sys.executable, ['python'] + sys.argv
    else:
        update.effective_message.reply_text(strings.stringAdminOnly)

def ip(bot, update):
    sender = update.message.from_user

    if sender.id == owner_id:
        res = requests.get("http://ipinfo.io/ip")
        ip = res.text  #  might need a .decode("utf-8") if you're using python 2. Test it!
        update.effective_message.reply_text("Server IP: " + ip)
    else:
        update.effective_message.reply_text(strings.stringAdminOnly)


def getid(bot, update):
    sender = update.message.from_user

    sender_id = str(sender.id)

    update.effective_message.reply_text("@" + sender.username + "'s ID is " + sender_id)


help_all = strings.help_message + strings.help_ip + strings.help_id


def save_note(bot, update, args):
    notes = loadjson(loc_notesjson)
    chat_id = str(update.message.chat_id)

    try:
        notes[chat_id]
    except KeyError:
        notes[chat_id] = {}

    if len(args) >= 2:
        # add note to note repo
        notename = args[0]
        del args[0]
        note_data = " ".join(args)
        notes[chat_id][notename] = note_data
        update.effective_message.reply_text("Added new note \"" + notename + "\" with content \"" + note_data + "\".")
    else:
        update.effective_message.reply_text(strings.errBadFormat)

    dumpjson(loc_notesjson, notes)


def get_note(bot, update, args):
    notes = loadjson(loc_notesjson)
    chat_id = str(update.message.chat_id)

    try:
        notes[chat_id]
    except KeyError:
        notes[chat_id] = {}

    if len(args) == 1:
        try:
            msg = notes[chat_id][args[0]]
        except KeyError:
            msg = strings.errNoNoteFound + args[0]

    else:
        msg = strings.errBadFormat
    update.effective_message.reply_text(msg)


def all_notes(bot, update, args):
    notes = loadjson(loc_notesjson)
    chat_id = str(update.message.chat_id)

    try:
        notes[chat_id]
    except KeyError:
        notes[chat_id] = {}

    msg = "No notes in this chat."
    if len(notes[chat_id]) > 0:
        msg = "These are the notes in the chat:\n"
        for note in notes[chat_id]:
            msg += "\n" + note

    update.effective_message.reply_text(msg)

@run_async
def reposync_xos(bot, update, args):
    sender = update.message.from_user

    string_args = ''.join(args)

    if sender.id == owner_id:
        if "fast" == string_args:
            update.effective_message.reply_text("User " + "@" + sender.username + " issued reposync fast command")

            subprocess.call("./data/scripts/xos/reposync_fast.sh")

            update.effective_message.reply_text("Reposync fast completed")
        else:
            update.effective_message.reply_text("User " + "@" + sender.username + " issued reposync command")

            subprocess.call("./data/scripts/xos/reposync.sh")

            update.effective_message.reply_text("Reposync fast completed")

    else:
        update.effective_message.reply_text(strings.stringAdminOnly)

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    updater = Updater(config.get("KEY", "tg_API_token"))

    os.remove(loc_restart_id)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler('restart_bot', restart))

    dispatcher.add_handler(CommandHandler("test", test))

    dispatcher.add_handler(CommandHandler("ip", ip))
    dispatcher.add_handler(CommandHandler("id", getid))

    dispatcher.add_handler(CommandHandler("save", save_note, pass_args=True))
    dispatcher.add_handler(CommandHandler("get", get_note, pass_args=True))
    dispatcher.add_handler(CommandHandler("note", all_notes, pass_args=True))

    dispatcher.add_handler(CommandHandler("reposync", reposync_xos, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
