import board
import math
from src import constants
import adafruit_as5600

class Encoder():
    def __init__(self):
        i2c = board.I2C()
        self._sensor = adafruit_as5600.AS5600(i2c)
        self._radius = constants.RADIUS
        self._prev_angle = 0.0

    def _get_angle(self):
        return self._sensor.angle

    def _diff_angle(self):
        angle = self._get_angle()
        delta = angle - self._prev_angle
        if delta > 180:
            delta -= 360
        elif delta < -180:
            delta += 360
        self._prev_angle = angle

    def clac_distance(self):
        delta = self._get_angle()
        distance = self._radius * math.radians(delta)
        return distance