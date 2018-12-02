import urllib


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

            params = urllib.urlencode(fields)

            f = urllib.urlopen("https://api.thingspeak.com/update", data=params)
        except Exception as e:
            print "Failed to submit data to ThingSpeak, reason = " + str(e)


class NullTarget(object):
    def submit(self, values):
        pass
