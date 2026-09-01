"""_summary_
検証用のメイン制御プログラム
"""
import threading
import time
from .motor.motor import Motor
from .motor.motor import ADJUST_DUTY_MODE
from .localization.get_location import IMUReceiver

imu = IMUReceiver()
mv = Motor(imu)
threading.Thread(target=mv.move, daemon=True).start()
mv.adjust_duty_cycle(ADJUST_DUTY_MODE.DIRECTION,direction="forward",sec=100)
end = time.time()+100
while time.time() < end:
    time.sleep(1)
mv.cleanup()

