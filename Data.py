from Metrics import AQI


class Pollutants(object):
    def __init__(self, pm2_5=0.0, pm10=0.0):
        self.pm_2_5 = pm2_5
        self.pm_10 = pm10


class PollutantsResult(object):
    def __init__(self, momentarily=Pollutants(), average=Pollutants()):
        self.momentarily = momentarily
        self.average = average
        self.aqi = (AQI(momentarily).get_index(), AQI(average).get_index())


def get_2_5_color_india(value):
    if value < 30:
        return "green"
    if value < 60:
        return "yellow green"
    if value < 90:
        return "yellow"
    if value < 120:
        return "orange"
    if value < 250:
        return "red"
    return "purple"


def get_2_5_color(value):
    if value < 15:
        return "green"
    if value < 30:
        return "yellow"
    if value < 55:
        return "orange"
    if value < 110:
        return "red"
    return "purple"


def get_10_color(value):
    if value < 25:
        return "green"
    if value < 50:
        return "yellow"
    if value < 90:
        return "orange"
    if value < 180:
        return "red"
    return "purple"


def get_10_color_india(value):
    if value < 50:
        return "green"
    if value < 100:
        return "yellow green"
    if value < 250:
        return "yellow"
    if value < 350:
        return "orange"
    if value < 430:
        return "red"
    return "purple"