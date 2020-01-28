#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from pathlib import Path
import logging
import yaml
import threading
import time

from sensor import Sensor

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

saveFolder = "save"
dataBaseFile = Path("data/punchTimes")

SENSOR_TIMEOUT = 0.2

def findById(objectWithId, listOfObjects, constructor):
    for obj in listOfObjects:
        if objectWithId.id == obj.id:
            return obj
    return constructor(objectWithId)

def getNewGroup(chat):
    saveFile = getSaveFileName(chat)
    if saveFile.is_file():
        with saveFile.open("r") as f:
            return yaml.load(f)
    else:
        return Group(chat)

def getSaveFileName(group):
    return Path(saveFolder, str(group.id))

    
class Group:
    def __init__(self, chat):
        self.id = chat.id
        self.numMembers = chat.get_members_count()
        self.players = []

class GuessBot:
    def __init__(self, sensor):
        self.sensor = sensor
        self.groups = []
        self.bot = None

    def getGroup(self, chat):
        group = findById(chat, self.groups, getNewGroup)
        if group not in self.groups:
            logger.info("Registering new group {}".format(group))
            self.groups.append(group)
        return group

    def error(self, bot, update, error):
        logger.warning('Update "%s" caused error "%s"', update, error)

    def help(self, bot, update):
        """You already know what this does."""
        group = self.getGroup(update.effective_chat)
        content = "\n".join("/{}: {}".format(name, command.__doc__) for (name, command) in self.commands)
        bot.send_message(chat_id=group.id, text=content)
        if group not in self.groups:
            self.groups.append(group)
        self.bot = bot

    def parseMessage(self, bot, update):
        assert update.effective_chat.type == "group"
        group = self.getGroup(update.effective_chat)
        group.save()
        print(self.bot, "i am here!!!")
        player = group.getPlayer(update.effective_user)
        content = update.message.text
        reply = self.processGuess(group, player, content)
        if reply is not None and reply != "":
            bot.send_message(chat_id=group.id, text=reply)

    def showStats(self, bot, update):
        group = self.getGroup(update.effective_chat)
        reply = str(self.data)
        bot.send_message(chat_id=group.id, text=reply)

    def readToken(self):
        with open("apiToken", "r") as f:
            return f.readlines()[0].replace("\n", "")

    def loadDatabase(self):
        with open(dataBaseFile, "r") as f:
            self.data = yaml.safe_load(f)

    def writeEntry(self):
        if self.bot is None:
            return
        for group in self.groups:
            self.bot.send_message(chat_id=group.id, text="SENSOR PRESSED")

    def sensorLoop(self):
        while True:
            self.sensor.read()
            time.sleep(SENSOR_TIMEOUT)
            if self.sensor.value == 1:
                self.writeEntry()

    def main(self):
        token = self.readToken()
        print(token)
        updater = Updater(token)

        self.loadDatabase()

        dispatcher = updater.dispatcher
        dispatcher.add_error_handler(self.error)
        self.commands = [
                ("help", self.help),
                ("showStats", self.showStats)
                ]

        for (name, command) in self.commands:
            dispatcher.add_handler(CommandHandler(name, command))
        dispatcher.add_handler(MessageHandler(Filters.group, self.parseMessage))

        t1 = threading.Thread(target=updater.start_polling)
        t2 = threading.Thread(target=self.sensorLoop)
        t1.start()
        t2.start()
        updater.idle()


if __name__ == '__main__':
    with Sensor() as sensor:
        print(sensor)
        bot = GuessBot(sensor)
        bot.main()
