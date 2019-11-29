#!/usr/bin/python3

import serial

logger = serial.Serial("/dev/ttyACM0", 9600)

while True:
    print('>> ', end="")
    cmd = input()
    logger.write(cmd)
    while logger.in_waiting:
        print(logger.read())
