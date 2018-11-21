import json


def read_config(meter_location_name):
    with open('AirMonitor.json') as config_file:
        data = json.load(config_file)

    meter = None
    all_meters = data["meters"]
    for m in all_meters:
        id = m['id']
        if id == meter_location_name:
            meter = m
            break

    return meter
