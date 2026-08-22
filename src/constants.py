from typing import Final

from src import configloading

confload = configloading.Config_reader()

UART_PORT:Final = confload.reader("arduino", "port", "character")
BAUDRATE:Final = confload.reader("arduino", "baudrate", "intenger")
