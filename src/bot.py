#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from pathlib import Path
import logging
import yaml
import threading
import time
import datetime
from contextlib import ExitStack

from src.sensor import Sensor
from src.game import Game, Player

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

saveFolder = "save"
dataBaseFile = Path("data/punchTimes")

SENSOR_TIMEOUT = 0.2

pinConfiguration = {3: "Toni", 5: "Peter"}

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

def saveDatabase(data, dataBasePath):
    with open(dataBasePath, "w") as f:
        yaml.dump(data, f)

def loadDatabase(dataBasePath):
    with open(dataBasePath, "r") as f:
        return yaml.safe_load(f)

class Group:
    def __init__(self, chat):
        self.id = chat.id
        self.numMembers = chat.get_members_count()
        self.players = []

class PunchBot:
    def __init__(self, sensors):
        self.sensors = sensors
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


    def writeEntry(self, message):
        if self.bot is None:
            return
        for group in self.groups:
            self.bot.send_message(chat_id=group.id, text=message)

    def sensorLoop(self):
        while True:
            for sensor in self.sensors:
                sensor.read()
            time.sleep(SENSOR_TIMEOUT)
            for sensor, player in zip(self.sensors, pinConfiguration.values()):
                if sensor.value == 1:
                    self.punchIn(Player(player))

    # def punchIn(self, bot, update):
    #     group = self.getGroup(update.effective_chat)
    #     player = Player(update.effective_user["first_name"])
    #     self.game.punchIn(player, datetime.datetime.today())
    #     saveDatabase(self.game.data, dataBaseFile)

    def punchIn(self, player):
        now = datetime.datetime.today()
        if self.game.punchIn(player, now):
            self.writeEntry("{} came in at {} today.".format(player.name, now.time()))
        saveDatabase(self.game.data, dataBaseFile)
    
    def main(self):
        token = self.readToken()
        updater = Updater(token)

        data = loadDatabase(dataBaseFile)
        self.game = Game(data)

        dispatcher = updater.dispatcher
        dispatcher.add_error_handler(self.error)
        self.commands = [
                ("help", self.help),
                ("showStats", self.showStats),
                ("punchIn", self.punchIn)
                ]

        for (name, command) in self.commands:
            dispatcher.add_handler(CommandHandler(name, command))
        dispatcher.add_handler(MessageHandler(Filters.group, self.parseMessage))

        t1 = threading.Thread(target=updater.start_polling)
        t2 = threading.Thread(target=self.sensorLoop)
        t1.start()
        t2.start()
        updater.idle()


def setupBot():
    with ExitStack() as stack:
        sensors = [stack.enter_context(Sensor(pin).__enter__()) for pin in pinConfiguration]
        bot = PunchBot(sensors)
        bot.main()

if __name__ == '__main__':
    setupBot()
