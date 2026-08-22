import serial
import time

from src import constants

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

if __name__ == "__main__":
    print("START")
    receiver = IMUReceiver()
    receiver.open()
    while True:
        try:
            print(receiver.getData())
        except Exception as e:
            print(e)
            break
    receiver.close()
