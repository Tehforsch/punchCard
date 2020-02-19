import yaml
import datetime

class Player:
    def __init__(self, name):
        self.name = name


class Game:
    def __init__(self, data):
        self.data = data

    def punchIn(self, player, date):
        self.data[player.name].append(date)

def saveDatabase():
    with open(self.dataBasePath, "w") as f:
        yaml.dump(self.data, f)

def loadDatabase():
    with open(self.dataBasePath, "r") as f:
        return yaml.safe_load(f)



game = Game("data/punchTimes")
print(game.data)
player = Player("Toni")
testDate = datetime.datetime(2020, 2, 25, 22, 22, 22) 
game.punchIn(player, testDate)
print(game.data)



