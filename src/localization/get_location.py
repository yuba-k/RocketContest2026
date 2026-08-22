import serial
import time

import constants

class IMUReceiver():
    def __init__(self) -> None:
        self._port = constants.UART_PORT
        self._baudrate = constants.BAUDRATE

    def open(self):
        self.ser = serial.Serial(self._port, self._baudrate)

    def getData(self):
        data = self.ser.readline().decode(errors="ignore")
        if data == "":
            return None
        return data.rstrip()

    def close(self):
        self.ser.close()