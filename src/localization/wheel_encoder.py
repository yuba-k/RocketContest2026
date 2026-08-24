import board

import adafruit_as5600

class Encoder():
    def __init__(self):
        i2c = board.I2C()
        self._sensor = adafruit_as5600.AS5600(i2c)

    def get_angle(self):
        return self._sensor.angle