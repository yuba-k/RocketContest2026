from src.localization import get_imu
from src.localization import wheel_encoder
import math
import time
import queue
import threading

class Location:
    def __init__(self) -> None:
        self.x, self.y = 0.0, 0.0
        self.latest_yaw = 0.0
        self.queue = queue.Queue(maxsize=1)
        self.imu = get_imu.IMUReceiver()
        self.imu.open()
        self.encoder = wheel_encoder.Encoder()
        self.isRunning = False
        self.hisLog = []

    def loop_start(self):
        self.isRunning = True
        threading.Thread(target=self.update_loop, daemon=True).start()

    def loop_stop(self):
        self.isRunning = False

    def update_loop(self):
        while self.isRunning:
            raw_line = self.imu.get_data(get_imu.DataMode.FULL)
            if raw_line != "None" and raw_line != "Empty":
                tmp = raw_line.split(",")
                roll = float(tmp[0].split(":")[1])
                pitch = float(tmp[1].split(":")[1])
                yaw = 180 + float(tmp[2].split(":")[1])
                degree = float(tmp[3].split(":")[1])
                self.latest_yaw = yaw
            d_left, d_right = self.encoder.get_delta_distance()
            d = (d_left + d_right)/2
            yaw_rad = math.radians(self.latest_yaw)
            self.x += d * math.cos(yaw_rad)
            self.y += d * math.sin(yaw_rad)
            self.hisLog.append(f"{tmp},x:{self.x},y:{self.y}")
            try:
                self.queue.get_nowait()
            except queue.Empty:
                pass
            self.queue.put_nowait(f"{self.x},{self.y},{self.latest_yaw}")
            time.sleep(0.02)

    def get_latest_yaw(self):
        return self.latest_yaw

def main():
    import src.motor.motor as motor
    locate = Location()
    locate.isRunning = True
    mv = motor.Motor()
    th1 = threading.Thread(target=locate.update_loop, daemon=True)
    th1.start()
    threading.Thread(target=mv.move, daemon=True).start()
    try:
        mv.adjust_duty_cycle(motor.ADJUST_DUTY_MODE.DIRECTION, direction="forward", duty=40)
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break
        with open("list.txt", "w") as f:
            for item in locate.hisLog:
                f.write(item + "\n")
    except Exception as e:
        print(e)
    finally:
        mv.cleanup()

if __name__ == "__main__":
    main()