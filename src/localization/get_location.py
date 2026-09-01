import serial
import time
import queue
import threading

from src import constants

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
        while self.stop_event:
            try:
                self.queue.put(self.ser.readline().decode(errors="ignore"))
            except queue.Full:
                pass
            time.sleep(0.01)

    def get_data(self):
        return self.queue.get()

    def close(self):
        self.stop_event.set()
        self.th1.join()
        self.ser.close()

if __name__ == "__main__":
    print("START")
    receiver = IMUReceiver()
    receiver.open()
    while True:
        try:
            print(receiver.get_data())
        except Exception as e:
            print(e)
            break
    receiver.close()
