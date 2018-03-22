from rideshare.geography.geopoint import GeoPoint
from rideshare.geography.path import PathEngine, MapPath
from rideshare.geography.path.client.osm_client import OSMClient


class OSMMapPath(MapPath):
    def __init__(self):
        super(OSMMapPath, self).__init__()
        self.client = OSMClient()

    def geocode(self, place):
        return self.client.geocode(place)

    def path_between(self, origin_search, destination_search):
        origin = origin_search if isinstance(origin_search, GeoPoint) else self.client.geocode(origin_search)
        destination = destination_search if isinstance(destination_search, GeoPoint) else self.client.geocode(
            destination_search)
        return self.client.find_route(origin, destination)


class OSMPathEngine(PathEngine):
    def get_points(self, result):
        """
        :type result: geography.path.client.osm_client.OSMPath
        :return:
        """
        return [GeoPoint(leg.latitude, leg.longitude) for leg in result.legs]

    @property
    def map_path(self):
        return OSMMapPath()
