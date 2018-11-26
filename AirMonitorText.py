import argparse
from Engine import AirMonitorEngine
from colorama import Fore, Style, init
from Data import get_2_5_color, get_10_color
from Metrics import Metrics, get_aqi_color
from ConfigReader import read_config
from Meters import create_smog_meter
from DataTargets import create_data_target
from time import sleep


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


def color_text_aqi(value):
    return (color_to_colorama(get_aqi_color(value))) + "{0:.0f}".format(value) + (Style.RESET_ALL)


def present_values_callback(values):
    aqi = "AQI = {} ({})".format(color_text_aqi(values.aqi[0]),
                                 color_text_aqi(values.aqi[1]))

    pm25 = " PM 2.5 = {} ({})".format(color_text_2_5(values.momentarily.pm_2_5),
                                      color_text_2_5(values.average.pm_2_5))

    pm10 = " PM 10 = {} ({})".format(color_text_10(values.momentarily.pm_10),
                                     color_text_10(values.average.pm_10))
    print aqi + pm25 + pm10
    sleep(0.5)


def main():
    init()
    parser = argparse.ArgumentParser(description='Air Monitor')
    parser.add_argument("location")
    arguments = parser.parse_args()
    config = read_config(arguments.location)
    engine = AirMonitorEngine(create_smog_meter(config["meter"], config["com_port"]),
                              create_data_target(config["target"], config["key"]),
                              present_values_callback,
                              Metrics(),
                              config["period_minutes"])

    while True:
        engine.probe()
        sleep(0.03)


if __name__ == "__main__":
    main()
