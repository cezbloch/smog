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


breakpoints_2_5 = (0.0, 12.0, 35.5, 55.5, 150.0, 250.0, 350.0, 500.5)
breakpoints_10  = (0.0, 55.0, 155.0, 255.0, 355.0, 425.0, 505.0, 605.0)
index_breakpoints = (0, 51, 101, 151, 201, 301, 401, 501)
labels = ("Good", "Moderate", "Unhealthy for Sensitive Groups", "Unhealthy", "Very Unhealthy", "Hazardous", "Death")


def calculate_aqi(value, levels):
    index = 0
    for level in levels:
        if value < level:
            c_low = levels[index]
            c_high = levels[index+1]
            i_low = index_breakpoints[index]
            i_high = index_breakpoints[index+1] - 1
            aqi = (i_high - i_low) * (value - c_low) / (c_high - c_low) + i_low
            return aqi


class AQI(object):
    def __init__(self, pollutants):
        self.pollutants = pollutants
        self.aqi_2_5 = calculate_aqi(self.pollutants.pm_2_5, breakpoints_2_5)
        self.aqi_10 = calculate_aqi(self.pollutants.pm_10, breakpoints_10)

    def get_index(self):
        aqi = max(self.aqi_2_5, self.aqi_10)
        return aqi



