import urllib.parse
import urllib.request


def create_data_target(target_type, key):
    if target_type == "NullTarget":
        return NullTarget()
    else:
        return ThingSpeakTarget(key)


class ThingSpeakTarget(object):
    def __init__(self, key):
        self.key = key

    def submit(self, values):
        try:
            fields = dict()
            fields['key'] = self.key
            field_id = 1
            for value in values:
                field_name = 'field' + str(field_id)
                fields[field_name] = "%.1f" % value
                field_id += 1

            params = urllib.parse.urlencode(fields).encode("utf-8")
            url_request = urllib.request.Request("https://api.thingspeak.com/update")
            urllib.request.urlopen(url_request, data=params)
        except Exception as e:
            print(f"Failed to submit data to ThingSpeak, reason = {e}")


class NullTarget(object):
    def submit(self, values):
        pass
