import configparser
import googlemaps
import polyline

from rideshare.geography.geopoint import GeoPoint
from rideshare.geography.path import MapPath, PathEngine
from rideshare.helper.util import make_absolute_path_to


class GoogleMapPath(MapPath):
    def __init__(self):
        super(GoogleMapPath, self).__init__()

        settings = configparser.ConfigParser()
        settings.read(make_absolute_path_to('config/settings.cfg'))
        key = settings.get('Google', 'key')

        self.map = googlemaps.Client(key=key)

    def path_between(self, origin, destination):
        return self.map.directions(origin, destination, mode="driving")

    def geocode(self, place):
        return self.map.geocode(place)


class GooglePathEngine(PathEngine):
    @property
    def map_path(self):
        return GoogleMapPath()


class GooglePolylinePathEngine(GooglePathEngine):
    def get_points(self, result):
        locations = polyline.decode(result[0]['overview_polyline']['points'])
        points = [GeoPoint(loc[0], loc[1]) for loc in locations]
        return points


class GoogleStepPathEngine(GooglePathEngine):
    def get_points(self, result):
        path = []
        for step in result[0]['legs'][0]['steps']:
            location = step['start_location']
            point = GeoPoint(location['lat'], location['lng'])
            path.append(point)
        return path
