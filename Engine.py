from Data import PollutantsResult
from Metrics import Metrics
import time


class AirMonitorEngine(object):
    def __init__(self, smog_meter, target, callback, period):
        self.metrics = Metrics()
        self.smog_meter = smog_meter
        self.callback = callback
        self.last_averages = None
        self.target = target
        self._period_minutes = float(period)

        self._time_of_last_update = time.time()

    def __del__(self):
        pass

    def probe(self):
        pollutants = self.smog_meter.get_values()

        if pollutants is None:
            return

        self.metrics.add_measurement(pollutants)

        seconds_in_minute = 60

        now = time.time()
        time_elapsed = (now - self._time_of_last_update)
        period_seconds = seconds_in_minute * self._period_minutes
        if time_elapsed > period_seconds:
            self.last_averages = self.metrics.average()
            self.target.submit(self.last_averages)
            self._time_of_last_update = time.time()

        result = PollutantsResult(pollutants, self.last_averages)
        self.callback(result)
