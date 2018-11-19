import serial
import re
import struct
from Data import Pollutants


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
