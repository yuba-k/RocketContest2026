import board
import math
from src import constants
import adafruit_as5600
import adafruit_tca9548a

class Encoder():
    def __init__(self):
        i2c = board.I2C()
        self._tca = adafruit_tca9548a.TCA9548A(i2c)
        self._sensor_left = adafruit_as5600.AS5600(self._tca[0])
        self._sensor_right = adafruit_as5600.AS5600(self._tca[1])
        self._radius = constants.RADIUS
        self.reset_base()

    def reset_base(self):
        self._prev_angle_left, self._prev_angle_right = self._get_angle()

    def _get_angle(self):
        return self._sensor_left.angle, self._sensor_right.angle

    @staticmethod
    def _angle_diff(current, previous):
        delta = current - previous

        if delta > 180:
            delta -=360
        elif delta < -180:
            delta += 360

        return delta

    def get_delta_distance(self):
        angle_left, angle_right = self._get_angle()

        delta_angle_left = self._angle_diff(
            angle_left,
            self._prev_angle_left
        )

        delta_angle_right = self._angle_diff(
            angle_right,
            self._prev_angle_right
        )

        self._prev_angle_left = angle_left
        self._prev_angle_right = angle_right

        distance_left = self._radius * math.radians(delta_angle_left)
        distance_right = self._radius * math.radians(delta_angle_right)

        return distance_left, distance_right