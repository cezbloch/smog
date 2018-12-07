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
        self.com_port = com_port
        self.port_name = self.com_port[:-1]
        self.port_number = 0
        self.buffer = ""
        self.inputPattern = re.compile('\\xAA.{17}\\xAB', re.DOTALL)
        self.serial_port = serial.Serial(self.com_port, 9600, timeout=0, parity=serial.PARITY_NONE, stopbits=1, bytesize=8)

    def reconnect(self):
        try:
            self.com_port = self.port_name + str(self.port_number)
            self.port_number += 1
            if self.port_number > 10:
                self.port_number = 0
            self.serial_port = serial.Serial(self.com_port, 9600, timeout=0, parity=serial.PARITY_NONE, stopbits=1, bytesize=8)
        except IOError as error:
            print "SDL607 failed to reconnect on port {} with error: {}".format(self.com_port, str(error))

    def get_values(self):
        try:
            while self.serial_port.inWaiting() > 0:
                bytes_amount = self.serial_port.inWaiting()
                self.buffer += self.serial_port.read(bytes_amount)
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
            self.reconnect()


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
