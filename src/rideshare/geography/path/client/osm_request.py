import math

from rideshare.geography.geopoint import GeoPoint


def special_floor(x, i=2):
    floored = math.floor(x)

    while floored % i != 0:
        floored -= 1

    return floored


class OSMMapAreaRequest(object):
    BOX_SIZE = 1.1  # u need to change floor()'s etc to match if u update this

    def __init__(self, loc1, loc2):
        super(OSMMapAreaRequest, self).__init__()
        min_lat, min_lng, max_lat, max_lng = make_bbox(loc1, loc2)

        lat = special_floor(min_lat, int(math.floor(self.BOX_SIZE)))

        self.boxes = []
        while lat < max_lat:
            next_lat = max_lat
            lng = special_floor(min_lng, int(math.floor(self.BOX_SIZE)))
            while lng < max_lng:
                box = self.__make_box(lat, lng)
                self.boxes.append(box)
                next_lat, lng = [special_floor(x, int(math.floor(self.BOX_SIZE))) for x in box[2:]]
            lat = next_lat

    def split(self, box):
        raise DeprecationWarning('Got some errors around equator that this might fix. Not tested')

        min_lat, min_lng, max_lat, max_lng = box

        offsets = [(0, 0, 1, 1),
                   (1, 0, 1, 1),
                   (1, 1, 1, 1),
                   (0, 1, 1, 1)]

        boxes = []
        for (bot, left, top, right) in offsets:
            boxes.append((min_lat + bot, min_lng + left, min_lat + top + self.BOX_SIZE, min_lng + right + self.BOX_SIZE))
        return boxes

        return

    def __make_box(self, lat, lng):
        return lat, lng, lat + self.BOX_SIZE, lng + self.BOX_SIZE

    def make_url(self, minlat=None, minlng=None, maxlat=None, maxlng=None):
        base_api_url = 'http://overpass-api.de/api'
        map_url = '%s/map?bbox=%s,%s,%s,%s' % (base_api_url, minlng, minlat, maxlng, maxlat)
        return map_url


def make_bbox(loc1, loc2, padding=10000):
    """
    :type padding: int
    :type loc1: GeoPoint
    :type loc2: GeoPoint
    :return:
    """
    minlng = min(loc1.lng, loc2.lng)
    minlat = min(loc1.lat, loc2.lat)
    south_west = GeoPoint(minlat, minlng).translate_meters(-padding, -padding)

    maxlng = max(loc1.lng, loc2.lng)
    maxlat = max(loc1.lat, loc2.lat)
    north_east = GeoPoint(maxlat, maxlng).translate_meters(padding, padding)

    result = south_west.lat, south_west.lng, north_east.lat, north_east.lng
    return result
