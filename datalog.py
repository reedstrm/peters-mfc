#!/usr/bin/python3
import os
import serial
from time import sleep
from datetime import datetime


datafile = open("data_log.csv", "a")
power_datafile = open("power_data_log.csv", "a")
tags = ["Time", "V0", "V1", "V2", "V3", "V4", "V5", "Temp", "Humi"]
power_tags = ["Time", "resistor_step", "V0", "V1", "V2", "V3", "V4", "V5"]
data = {}

if os.stat("data_log.csv").st_size == 0:
        datafile.write(",".join(tags)+"\n")

if os.stat("power_data_log.csv").st_size == 0:
        power_datafile.write(",".join(power_tags)+"\n")

logger = serial.Serial('/dev/ttyACM0', 9600, timeout=60)

sleep(10)  # Wait for arduino to boot


def main():
    power_count = 0
    while True:
        read_volts()
        power_count += 1
        if power_count == 12:
            power_count = 0
            read_power()  # takes ~ 3.5 min
            sleep(90)
        else:
            sleep(300)


def read_volts():
    logger.flushInput()
    logger.write(b"V")
    print("Reading volts")
    for k in data:
        data[k] = None
    data["Time"] = str(datetime.now()).encode()
    tag = "nada"
    sleep(1)

    while tag != b"Humi":
        dataline = logger.readline()
        if dataline == b"":
            exit(1)
        tag, value = dataline.split(maxsplit=2)
        data[tag.decode()] = value

    datafile.write(",".join([data[t].decode() for t in tags])+"\n")
    datafile.flush()


def read_power():
    logger.flushInput()
    logger.write(b"P")
    logger.flushOutput()
    res_val = 999999
    print("Reading power")
    while res_val != "0":
        dataline = logger.readline().decode()
        if dataline == "":
            exit(1)
        power_data = [str(datetime.now())]
        power_data.extend(dataline.split())
        res_val = power_data[1]
        print (res_val)
        power_datafile.write(",".join(power_data)+"\n")
        power_datafile.flush()


if __name__ == '__main__':
    main()
