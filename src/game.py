import yaml
import datetime

class PlayerNotFoundError(Exception):
    pass


class Player:
    def __init__(self, name):
        self.name = name


class Game:
    def __init__(self, data):
        self.data = data

    def punchIn(self, player, date):
        if not player.name in self.data:
            raise PlayerNotFoundError
        
        if date.date() in (tempdate.date() for tempdate in self.data[player.name]):
            return False
        self.data[player.name].append(date)
        return True

def saveDatabase(data, dataBasePath):
    with open(dataBasePath, "w") as f:
        yaml.dump(data, f)

def loadDatabase(dataBasePath):
    with open(dataBasePath, "r") as f:
        return yaml.safe_load(f)



# data = loadDatabase("data/punchTimes")
# game = Game(data)
# print(game.data)
# player = Player("Toni")
# testDate = datetime.datetime(2020, 2, 25, 22, 22, 22) 
# game.punchIn(player, testDate)
# print(game.data)



