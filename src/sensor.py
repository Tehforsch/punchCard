# import RPi.GPIO as GPIO
from time import sleep
import sys
import time

class Sensor:
    def __init__(self, pin):
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(TOUCH_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.pin = pin
        self.initial_time = time.time()

    def readStopSensor(self, sensor):
        # return GPIO.input(sensor)
        pass
     
    def cleanup(self):
        # GPIO.cleanup()
        pass

    def read(self):
        # self.value = self.readStopSensor(TOUCH_SENSOR)
        print(self.pin, time.time() - self.initial_time)
        self.value = int(time.time() - self.initial_time > 5*self.pin)
        return self.value

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.cleanup()
        print("Sensor cleaned up")

if __name__ == "__main__":
    sensor = Sensor()
    while True:
        print(sensor.readStopSensor(TOUCH_SENSOR))
