import numpy as np


class Metrics(object):
    def __init__(self):
        self.samples = None

    def add_measurement(self, pollutants):
        if self.samples is None:
            self.samples = np.array(pollutants)
        else:
            self.samples = np.vstack((self.samples, np.array([pollutants])))

    def average(self):
        average = self.samples.mean(axis=0)
        self.samples = None
        return average


breakpoints_2_5 = (0.0, 12.0, 35.5, 55.5, 150.0, 250.0, 350.0, 500.5)
breakpoints_10 = (0.0, 55.0, 155.0, 255.0, 355.0, 425.0, 505.0, 605.0)
breakpoints_aqi = (0, 51, 101, 151, 201, 301, 401, 501)
labels = ("Good", "Moderate", "Unhealthy for Sensitive Groups", "Unhealthy", "Very Unhealthy", "Hazardous", "Death")
colors = ("green", "yellow", "orange", "red", "purple", "maroon", "maroon", "black")


def get_color(value, breakpoints):
    index = 0
    for low in breakpoints:
        if value < low:
            return colors[index]
        index += 1
    raise IndexError


def get_2_5_color(value):
    return get_color(value, breakpoints_2_5)


def get_10_color(value):
    return get_color(value, breakpoints_10)


def get_aqi_color(value):
    return get_color(value, breakpoints_aqi)


def calculate_aqi(value, levels):
    index = 0
    for level in levels:
        if value <= level:
            c_low = levels[index - 1]
            c_high = levels[index]
            i_low = breakpoints_aqi[index - 1]
            i_high = breakpoints_aqi[index] - 1
            aqi = (i_high - i_low) * (value - c_low) / (c_high - c_low) + i_low
            return aqi
        index += 1
    raise IndexError


class AQI(object):
    def __init__(self, pm_2_5, pm_10):
        self.aqi_2_5 = calculate_aqi(pm_2_5, breakpoints_2_5)
        self.aqi_10 = calculate_aqi(pm_10, breakpoints_10)

    def get_index(self):
        aqi = max(self.aqi_2_5, self.aqi_10)
        return aqi
