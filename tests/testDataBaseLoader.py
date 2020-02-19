import unittest
from src.game import loadDatabase

class TestDataBase(unittest.TestCase):
    def setUp(self):
        pass

    def test_load(self):
        data = loadDatabase("tests/sampleData")
        assert len(data.keys()) == 2

if __name__ == '__main__':
    unittest.main()
