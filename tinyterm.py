#!/usr/bin/python3
import serial
import sys
import select

logger = serial.Serial("/dev/ttyACM0", 9600)


print('>> ', end="", flush=True)
while True:
    i, o, e = select.select( [sys.stdin], [], [], 1 )
    if (i):
        cmd = sys.stdin.readline()
        if cmd[0] != 'O':
            logger.write(cmd[0].encode("ascii"))
        else:
            logger.write(cmd.encode("ascii"))
        print('>> ', end="", flush=True)
    while logger.inWaiting():
        print(logger.readline().decode(), end="")
