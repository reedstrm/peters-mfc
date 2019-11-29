import os
import serial
from time import sleep
from datetime import datetime


datafile = open("data_log.csv", "a")
tags = ["Time", "V0", "V1", "V2", "V3", "V4", "V5", "Temp", "Humi"]
data = {}

if os.stat("data_log.csv").st_size == 0:
        datafile.write(",".join(tags)+"\n")

logger = serial.Serial('/dev/ttyACM0', 9600)

while True:
    logger.flushInput()
    for k in data:
        data[k] = None
    data["Time"] = str(datetime.now()).encode()
    tag = "nada"
    while tag != b"V0":
        dataline = logger.readline()
        try:
            tag, value = dataline.split(maxsplit=2)
            data[tag] = value
        except ValueError:
            pass

    while tag != b"Humi":
        dataline = logger.readline()
        tag, value = dataline.split(maxsplit=2)
        data[tag] = value

    datafile.write(",".join([data[t].decode() for t in data])+"\n")
    datafile.flush()
    sleep(60)
