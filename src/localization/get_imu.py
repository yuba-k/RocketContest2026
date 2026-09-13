import serial
import time
import queue
import threading
from typing import List

from src import constants

class DataMode():
    FULL = 1
    YAW = 2

class IMUReceiver():
    def __init__(self) -> None:
        self._port = constants.UART_PORT
        self._baudrate = constants.BAUDRATE
        self.queue = queue.Queue(maxsize=1)
        self.stop_event = threading.Event()

    def open(self):
        self.ser = serial.Serial(self._port, self._baudrate)
        self.run = True
        self.th1 = threading.Thread(target=self.update_loop,daemon=True)
        self.th1.start()

    def update_loop(self):
        while not self.stop_event.is_set():
            data = self.ser.readline().decode(errors="ignore")
            try:
                self.queue.get_nowait()
            except queue.Empty:
                pass
            self.queue.put_nowait(data)
            time.sleep(0.01)

    def get_data(self, mode) -> str:
        try:
            if mode == DataMode.FULL:
                return self.queue.get_nowait()
            elif mode == DataMode.YAW:
                data = self.queue.get_nowait()
                yaw = data.split(",")[2]
                return yaw.split(":")[1]
            else:
                raise Exception("That mode does not exist.")
        except queue.Empty:
            return "Empty"
        except Exception as e:
            print(e)
            return "None"

    def close(self):
        self.stop_event.set()
        self.th1.join()
        self.ser.close()

if __name__ == "__main__":
    try:
        print("START")
        receiver = IMUReceiver()
        receiver.open()
        while True:
            try:
                print(receiver.get_data(DataMode.FULL))
            except Exception as e:
                print(e)
                raise KeyboardInterrupt
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        receiver.close()
