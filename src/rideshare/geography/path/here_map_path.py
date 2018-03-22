import configparser

from rideshare.geography.geopoint import GeoPoint
from rideshare.geography.path import MapPath, PathEngine
from rideshare.geography.path.client.heremaps_client import HereMapsClient
from rideshare.helper.util import make_absolute_path_to


class HereMapPath(MapPath):
    def geocode(self, place):
        return self.client.geocode(place)

    def __init__(self):
        super(HereMapPath, self).__init__()

        settings = configparser.ConfigParser()
        settings.read(make_absolute_path_to('config/settings.cfg'))
        app_id = settings.get('HERE', 'app_id')
        app_code = settings.get('HERE', 'app_code')
        self.client = HereMapsClient(app_id, app_code)

    def path_between(self, origin_search, destination_search):
        origin = self.client.geocode(origin_search)
        destination = self.client.geocode(destination_search)

        return self.client.route(origin, destination)


class HerePathEngine(PathEngine):
    @property
    def map_path(self):
        return HereMapPath()

    def get_points(self, result):
        if not result['leg']:
            return []

        points = []
        for maneuver in result['leg'][0]['maneuver']:
            position = maneuver['position']
            points.append(GeoPoint(position['latitude'], position['longitude']))
        return points
