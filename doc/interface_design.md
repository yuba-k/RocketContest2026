---
title: インターフェース仕様書
---
# 1. Interface Overview
```mermaid
flowchart LR
    RaspberryPi["Raspberry Pi Zero 2 W"]
    Arduino["Arduino Pro Mini"]
    IMU["9軸センサ<br/>Pololu 2738"]
    MUX["I2C Multiplexer<br/>TCA9548A"]
    LeftEncoder["Left Encoder<br/>AS5600"]
    RightEncoder["Right Encoder<br/>AS5600"]
    Camera["Raspberry Pi AI Camera"]

    RaspberryPi <-->|UART| Arduino
    Arduino <-->|I2C| IMU

    RaspberryPi -->|I2C| MUX
    MUX -->|I2C Channel 0| LeftEncoder
    MUX -->|I2C Channel 1| RightEncoder

    RaspberryPi -->|MIPI CSI| Camera
```
# 2. Interface List

|ID|Device A|Device B|Interface|Direction|
|---|---|---|---|---|
|IF-001|RaspberryPiZero2W|ArduinoProMini|UART|Bidirectional|
|IF-002|ArduinoProMini|Pololu-2738|I2C|Bidirectional|
|IF-003|RaspberryPiZero2W|TCA9548A|I2C|Bidirectional|
|IF-004|TCA9548A(0x70)|AS5600|I2C|Bidirectional|
|TF-005|TCA9548A(0x71)|AS5600|I2C|Bidirectional|
|TF-006|RaspberryPiZero2W|RaspberryPiAICamera|CSI|Bidirectional|