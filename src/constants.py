from typing import Final

from src import configloading

confload = configloading.Config_reader()

UART_PORT:Final = confload.reader("arduino", "port", "character")
BAUDRATE:Final = confload.reader("arduino", "baudrate", "intenger")
RADIUS:Final = confload.reader("hard", "radius", "float")

DUTY: Final = confload.reader("motor", "duty", "intenger")
BASE_DUTY: Final = confload.reader("motor", "base_duty", "intenger")
RIGHT_PWM: Final = confload.reader("motor", "right_pwm", "intenger")
RIGHT_PHASE: Final = confload.reader("motor", "right_phase", "intenger")
LEFT_PWM: Final = confload.reader("motor", "left_pwm", "intenger")
LEFT_PHASE: Final = confload.reader("motor", "left_phase", "intenger")

KP: Final = confload.reader("pid", "kp", "float")
KI: Final = confload.reader("pid", "ki", "float")
KD: Final = confload.reader("pid", "kd", "float")