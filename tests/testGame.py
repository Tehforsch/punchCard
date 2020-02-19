import unittest
import datetime
from src.game import Game, Player, PlayerNotFoundError, loadDatabase

class TestDataBase(unittest.TestCase):
    def setUp(self):
        self.data = loadDatabase("tests/sampleData")
        self.player1 = Player("Herbert")
        self.player2 = Player("Toni")
        self.game = Game(self.data)
        self.date = datetime.datetime(2020, 2, 25, 22, 22, 22)
        
    def testPunchInWrongPlayer(self):
        try:
            self.game.punchIn(self.player1, self.date)
        except PlayerNotFoundError:
            pass
        else:
            assert False

    def testPunchInCorrectPlayer(self):
        self.game.punchIn(self.player2, self.date)

    def testPunchInCorrectDate(self):
        self.game.punchIn(self.player2, self.date)
        date_entered = self.game.data[self.player2.name][-1]
        assert date_entered == self.date

    def testPunchInTwice(self):
        self.game.punchIn(self.player2, self.date)
        self.game.punchIn(self.player2, datetime.datetime(2020, 2, 25, 21, 20, 20))
        assert len([tempdate for tempdate in self.game.data[self.player2.name] if tempdate.date() == self.date.date()]) == 1


if __name__ == '__main__':
    unittest.main()
