import argparse
from Engine import AirMonitorEngine
from colorama import Fore, Back, Style, init
from Data import get_2_5_color, get_10_color


def color_to_colorama(color):
    if color == "green":
        return Fore.GREEN
    if color == "yellow":
        return Fore.YELLOW
    if color == "orange":
        return Fore.LIGHTYELLOW_EX
    if color == "red":
        return Fore.RED
    return Fore.LIGHTRED_EX


def color_text_2_5(value):
    return (color_to_colorama(get_2_5_color(value))) + "{0:.1f}".format(value) + (Style.RESET_ALL)


def color_text_10(value):
    return (color_to_colorama(get_10_color(value))) + "{0:.1f}".format(value) + (Style.RESET_ALL)


def present_values_callback(values):
    pm25 = "PM 2.5 = " + color_text_2_5(values.momentarily.pm_2_5) + " ({})".format(color_text_2_5(values.average.pm_2_5))
    pm10 = " PM 10 = " + color_text_10(values.momentarily.pm_10) + " ({})".format(color_text_10(values.average.pm_10))
    print pm25 + pm10


def main():
    init()
    parser = argparse.ArgumentParser(description='Air Monitor')
    parser.add_argument("location")
    parser.add_argument("--test")
    arguments = parser.parse_args()
    engine = AirMonitorEngine(arguments, present_values_callback)
    engine.loop()


if __name__ == "__main__":
    main()
