from SDL607 import SDL607
from FakeMeter import FakeMeter
from Data import Pollutants, PollutantsResult
import json
import time
import numpy as np
import urllib


def create_smog_meter(test_mode, port):
    if test_mode:
        return FakeMeter()
    else:
        return SDL607(port)


class AirMonitorEngine(object):
    def __init__(self, arguments, callback):
        self.callback = callback
        self.last_averages = Pollutants()
        self.test_mode = arguments.test is not None

        with open('AirMonitor.json') as config_file:
            data = json.load(config_file)

        meter = None
        all_meters = data["meters"]
        for m in all_meters:
            id = m['id']
            if id == arguments.location:
                meter = m
                break

        if meter is None:
            raise "Invalid configuration file or argument"

        com_port = meter["com_port"]
        is_test_mode = arguments.test is not None
        self.smog_meter = create_smog_meter(is_test_mode, com_port)
        self._thingspeak_key = meter["key"]
        self._period_minutes = float(meter["period_minutes"])

        self.samples = None
        self._time_of_last_update = time.time()

        self.outCsv = open('AirMonitor.csv','w')
        self.updateNo = 0

    def __del__(self):
        self.outCsv.close()

    def loop(self):
        while True:
            self.updateNo = self.updateNo + 1

            pollutants = self.smog_meter.get_values()

            if pollutants is None:
                continue

            if self.samples is None:
                self.samples = np.array([pollutants.pm_2_5, pollutants.pm_10])
            else:
                self.samples = np.vstack((self.samples, np.array([[pollutants.pm_2_5, pollutants.pm_10]])))

            seconds_in_minute = 60

            if not self.test_mode:
                now = time.time()
                time_elapsed = (now - self._time_of_last_update)
                period_seconds = seconds_in_minute * self._period_minutes
                if time_elapsed > period_seconds:
                    average = self.samples.mean(axis=0)
                    self.last_averages = Pollutants(average[0], average[1])
                    params = urllib.urlencode({'key': self._thingspeak_key, 'field1': "%.1f"% self.last_averages.pm_2_5, 'field2':"%.1f"% self.last_averages.pm_10})
                    f = urllib.urlopen("https://api.thingspeak.com/update", data=params)
                    self.updateNo = 0
                    self.samples = None
                    self._time_of_last_update = time.time()

            result = PollutantsResult(pollutants, self.last_averages)
            self.callback(result)
