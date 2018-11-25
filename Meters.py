import serial
import re
import struct
from Data import Pollutants
import random
from time import time


def create_smog_meter(meter_type, port):
    if meter_type == "FakeMeter":
        return FakeMeter()
    else:
        return SDL607(port)


class SDL607(object):
    def __init__(self, com_port):
        self.serial_port = serial.Serial(com_port, 9600, timeout=0, parity=serial.PARITY_NONE, stopbits=1, bytesize=8)
        self.buffer = ""
        self.inputPattern = re.compile('\\xAA.{17}\\xAB', re.DOTALL)

    def get_values(self):
        while self.serial_port.inWaiting() > 0:
            l = self.serial_port.inWaiting()
            self.buffer += self.serial_port.read(l)
            m = self.inputPattern.match(self.buffer)
            if m:
                data = self.buffer[m.start():m.end()]
                self.buffer = self.buffer[m.end():]
                udata = struct.unpack('<cHHHHHHHHcc', data)

                udata2 = udata[2] / 10.0
                udata3 = udata[3] / 10.0
                udata4_pm_25 = udata[4] / 10.0
                udata5 = udata[5] / 10.0
                udata6_pm_10 = udata[6] / 10.0
                udata7 = udata[7] / 10.0
                udata8 = udata[8] / 10.0

                pollutants = Pollutants()
                pollutants.pm_2_5 = udata4_pm_25
                pollutants.pm_10 = udata6_pm_10

                return pollutants
            return None


class FakeMeter(object):
    def __init__(self):
        self.last_update_time = time()
        self.period_in_seconds = 1

    def get_values(self):
        now = time()
        time_elapsed = now - self.last_update_time
        if time_elapsed > self.period_in_seconds:
            pollutants = Pollutants()
            pollutants.pm_2_5 = random.uniform(1.0, 200.0)
            pollutants.pm_10 = random.uniform(1.0, 300.0)
            self.last_update_time = time()
            return pollutants

        return None

