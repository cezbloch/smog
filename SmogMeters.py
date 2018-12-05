import serial
import re
import struct
import random
from time import time
from Metrics import AQI


def create_smog_meter(meter_type, port):
    if meter_type == "FakeMeter":
        return AqiMeterDecorator(FakeMeter())
    else:
        return AqiMeterDecorator(SDL607(port))


class AqiMeterDecorator(object):
    def __init__(self, meter):
        self.meter = meter

    def get_values(self):
        values = self.meter.get_values()
        if values is not None:
            aqi = AQI(values[0], values[1]).get_index()
            values.append(aqi)

        return values


class SDL607(object):
    def __init__(self, com_port):
        self.serial_port = serial.Serial(com_port, 9600, timeout=0, parity=serial.PARITY_NONE, stopbits=1, bytesize=8)
        self.buffer = ""
        self.inputPattern = re.compile('\\xAA.{17}\\xAB', re.DOTALL)

    def get_values(self):
        try:
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

                    return [udata4_pm_25, udata6_pm_10]
                return None
        except IOError as error:
            print "SDL607 failed to read value with error: {}".format(str(error))


class FakeMeter(object):
    def __init__(self):
        self.last_update_time = time()
        self.period_in_seconds = 1

    def get_values(self):
        now = time()
        time_elapsed = now - self.last_update_time
        if time_elapsed > self.period_in_seconds:
            pm_2_5 = random.uniform(1.0, 200.0)
            pm_10 = random.uniform(1.0, 300.0)
            self.last_update_time = time()
            return [pm_2_5, pm_10]

        return None
