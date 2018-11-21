import numpy as np


class Metrics(object):
    def __init__(self):
        self.samples = None

    def add_measurement(self, pollutants):
        if self.samples is None:
            self.samples = np.array([pollutants.pm_2_5, pollutants.pm_10])
        else:
            self.samples = np.vstack((self.samples, np.array([[pollutants.pm_2_5, pollutants.pm_10]])))

    def average(self):
        average = self.samples.mean(axis=0)
        self.samples = None
        return average
