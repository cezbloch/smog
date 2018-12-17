import unittest
from Metrics import AQI, get_2_5_color


class TestAQI(unittest.TestCase):

    def test_good(self):
        aqi = AQI(6, 10)
        index = aqi.get_index()
        self.assertEqual(index, 25)

    def test_good_edge(self):
        aqi = AQI(12, 10)
        index = aqi.get_index()
        self.assertEqual(index, 50)

    def test_gets_correct_color_for_good_quality(self):
        color = get_2_5_color(8.0)
        self.assertEqual(color, "green")


if __name__ == '__main__':
    unittest.main()