from Data import Pollutants
import random


class FakeMeter(object):
    def __init__(self):
        self.iteration = 0

    def get_values(self):
        if self.iteration % 60 == 0:
            pollutants = Pollutants()
            pollutants.pm_2_5 = random.uniform(1.0, 500.0)
            pollutants.pm_10 = random.uniform(1.0, 500.0)
            return pollutants

        return None

