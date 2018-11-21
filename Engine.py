from Data import Pollutants, PollutantsResult
import time


class AirMonitorEngine(object):
    def __init__(self, smog_meter, target, callback, metrics, period):
        self.metrics = metrics
        self.smog_meter = smog_meter
        self.callback = callback
        self.last_averages = Pollutants()
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
            average = self.metrics.average()
            self.last_averages = Pollutants(average[0], average[1])
            self.target.submit(self.last_averages)
            self._time_of_last_update = time.time()

        result = PollutantsResult(pollutants, self.last_averages)
        self.callback(result)

    def loop(self):
        while True:
            self.probe()
            time.sleep(1)

