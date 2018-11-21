import urllib


class ThingSpeakTarget(object):
    def __init__(self, key):
        self.key = key

    def submit(self, pollutants):
        try:
            params = urllib.urlencode({'key': self.key, 'field1': "%.1f" % pollutants.pm_2_5,
                                       'field2': "%.1f" % pollutants.pm_10})
            f = urllib.urlopen("https://api.thingspeak.com/update", data=params)
        except Exception as e:
            print "Failed to submit data to ThingSpeak, reason = " + str(e)


class NullTarget(object):
    def submit(self, pollutants):
        pass
