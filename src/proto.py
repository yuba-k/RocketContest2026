"""_summary_
検証用のメイン制御プログラム
"""
import motor.motor as motor
import localization.get_location as get_location

imu = get_location.IMUReceiver()
mv = motor.Motor(imu)
