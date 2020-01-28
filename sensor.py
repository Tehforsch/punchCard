import RPi.GPIO as GPIO
from time import sleep
import sys
import time

TOUCH_SENSOR = 2

class Sensor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TOUCH_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def readStopSensor(self, sensor):
        return GPIO.input(sensor)
     
    def cleanup(self):
        GPIO.cleanup()

    def read(self):
        self.value = self.readStopSensor(TOUCH_SENSOR)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.cleanup()
        print("Sensor cleaned up")

if __name__ == "__main__":
    sensor = Sensor()
    while True:
        print(sensor.readStopSensor(TOUCH_SENSOR))
