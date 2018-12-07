import argparse
from Engine import AirMonitorEngine
from colorama import Fore, Style, init
from Metrics import get_aqi_color, get_2_5_color, get_10_color
from ConfigReader import read_config
from SmogMeters import create_smog_meter
from WeatherMeters import create_weather_meter
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


def color_average_and_momentary(values, index):
    momentary = color_text_aqi(values.momentarily[index])
    average = "-"
    if values.average is not None:
        average = color_text_aqi(values.average[index])
    text = "= {} ({})".format(momentary, average)
    return text


display_values = True


def present_values_callback(values):
    if display_values:
        aqi = "AQI = " + color_average_and_momentary(values, 2)

        pm25 = " PM 2.5 = " + color_average_and_momentary(values, 0)

        pm10 = " PM 10 = " + color_average_and_momentary(values, 1)
        print aqi + pm25 + pm10
    sleep(0.5)


def present_weather_callback(values):
    if display_values:
        print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(values.momentarily[0], values.momentarily[1])


def main():
    init()
    parser = argparse.ArgumentParser(description='Air Monitor')
    parser.add_argument("location")
    parser.add_argument('-s', '--silent', action='store_true')
    arguments = parser.parse_args()
    global display_values
    display_values = not arguments.silent
    config = read_config(arguments.location)
    engines = []

    if "meter" in config.keys():
        smog_engine = AirMonitorEngine(create_smog_meter(config["meter"], config["com_port"]),
                                       create_data_target(config["target"], config["key"]),
                                       present_values_callback,
                                       config["period_minutes"])
        engines.append(smog_engine)

    if "weather_meter" in config.keys():
        weather_engine = AirMonitorEngine(create_weather_meter(config["weather_meter"]),
                                          create_data_target(config["target"], config["weather_key"]),
                                          present_weather_callback,
                                          config["period_minutes"])
        engines.append(weather_engine)

    while True:
        for engine in engines:
            engine.probe()

        sleep(0.03)


if __name__ == "__main__":
    main()
