import datetime
import yaml
import json

#timesDict = {'Peter': {datetime.datetime(2020, 1, 22): datetime.time(8, 50), datetime.date(2020, 1, 23): datetime.time(8, 58), datetime.date(2020, 1, 24): datetime.time(8, 50), datetime.date(2020, 1, 27): datetime.time(8, 59), datetime.date(2020, 1, 28): datetime.time(8, 56)}, 'Toni': {datetime.date(2020, 1, 22): datetime.time(8, 56), datetime.date(2020, 1, 23): datetime.time(8, 52), datetime.date(2020, 1, 24): datetime.time(8, 50), datetime.date(2020, 1, 27): datetime.time(8, 41), datetime.date(2020, 1, 28): datetime.time(8, 55)}}
timesDict = {
        'Peter':
            [datetime.datetime(2020, 1, 22, 8, 50),
            datetime.datetime(2020, 1, 23, 8, 58),
            datetime.datetime(2020, 1, 24, 8, 50),
            datetime.datetime(2020, 1, 27, 8, 59),
            datetime.datetime(2020, 1, 28, 8, 56)],
        'Toni':
            [datetime.datetime(2020, 1, 22, 8, 56),
            datetime.datetime(2020, 1, 23, 8, 52),
            datetime.datetime(2020, 1, 24, 8, 50),
            datetime.datetime(2020, 1, 27, 8, 41),
            datetime.datetime(2020, 1, 28, 8, 55)]
            }

def main():
    with open("../data/punchTimes", "w") as f:
        print("??? hello??")
        yaml.dump(timesDict, f)

main()
