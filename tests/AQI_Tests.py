import unittest
from Data import Pollutants
from Metrics import AQI


class TestAQI(unittest.TestCase):

    def test_good(self):
        aqi = AQI(Pollutants(6, 10))
        index = aqi.get_index()
        self.assertEqual(index, 25)

    def test_good_edge(self):
        aqi = AQI(Pollutants(12, 10))
        index = aqi.get_index()
        self.assertEqual(index, 50)


if __name__ == '__main__':
    unittest.main()