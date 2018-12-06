from time import time, sleep
import random


def create_weather_meter(meter_type):
    if meter_type == "FakeTemperaturePressureMeter":
        return FakeTemperaturePressureMeter()
    else:
        return DHT11TemperaturePressureMeter()


class FakeTemperaturePressureMeter(object):
    def __init__(self):
        self.last_update_time = time()
        self.period_in_seconds = 3

    def get_values(self):
        now = time()
        time_elapsed = now - self.last_update_time
        if time_elapsed > self.period_in_seconds:
            temperature = random.uniform(-20.0, 40.0)
            humidity = random.uniform(0.0, 100.0)
            self.last_update_time = time()
            return [temperature, humidity]

        return None


class DHT11TemperaturePressureMeter(object):
    def __init__(self):
        self.dht_11_sensor_id = 11
        self.gpio_port = 4

    def get_values(self):
        try:
            import Adafruit_DHT
            humidity, temperature = Adafruit_DHT.read(self.dht_11_sensor_id, self.gpio_port)
            if humidity is None or temperature is None:
                return None

            return [temperature, humidity]
        except IOError as error:
            print "DHT11 failed to read value with error: {}".format(str(error))


def main():
    #meter = FakeTemperaturePressureMeter()
    meter = DHT11TemperaturePressureMeter()
    while True:
        values = meter.get_values()
        if values is not None:
            print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(values[0], values[1])
        else:
            print '-'

        sleep(0.5)


if __name__ == "__main__":
    main()
