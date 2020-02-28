import RPi.GPIO as GPIO
from time import sleep
import sys
import time

class Sensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def cleanup(self):
        GPIO.cleanup()

    def read(self):
        self.value = GPIO.input(self.pin)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.cleanup()
        print("Sensor cleaned up")

if __name__ == "__main__":
    sensor = Sensor(2)
    while True:
        sensor.read()
        print(sensor.value)
