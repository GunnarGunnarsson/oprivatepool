import json

import requests

from rideshare.geography.geopoint import GeoPoint

# import json
from xml.etree import ElementTree


class HereMapsClient(object):
    GEOCODE_URL = "https://geocoder.cit.api.here.com/6.2/geocode.xml?gen=9&"
    ROUTE_URL = "https://route.api.here.com/routing/7.2/calculateroute.json?mode=fastest;car;traffic:disabled"

    POSITION_XPATH = 'Response/View/Result/Location/NavigationPosition'

    def __init__(self, app_id, app_code):
        self.app_id = app_id
        self.app_code = app_code

    def geocode(self, search):
        url = self.__create_geocode_request(search)

        position = ElementTree.fromstring(requests.get(url).content).find(self.POSITION_XPATH)

        if position is None:
            raise ValueError("Couldn't locate '%s'" % search)

        return HereWaypoint(GeoPoint(position.find('Latitude').text, position.find('Longitude').text))

    def route(self, origin, dest):
        url = self.__create_route_request_url(origin, dest)
        response = requests.get(url)
        route = json.loads(response.content)['response']['route'][0]
        return route

    def __create_route_request_url(self, origin_waypoint, destination_waypoint):
        url = '%s&waypoint0=%s&waypoint1=%s' % (self.ROUTE_URL, origin_waypoint, destination_waypoint)
        return self.__finish(url)

    def __create_geocode_request(self, search):
        url = "%s&searchtext=%s" % (self.GEOCODE_URL, search)
        return self.__finish(url)

    def __finish(self, url):
        return self.__urlencode(self.__authenticate(url))

    def __authenticate(self, url):
        credentials = "&app_id=%s&app_code=%s" % (self.app_id, self.app_code)
        return url + credentials

    def __urlencode(self, url):
        return url


class HereWaypoint(GeoPoint):
    def __init__(self, point):
        super(HereWaypoint, self).__init__(point.lat, point.lng)

    def __repr__(self):
        return 'geo!%s,%s' % (self.lat, self.lng)

    def __str__(self):
        return repr(self)
