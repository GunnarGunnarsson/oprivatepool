import json
import math

from hos_protocol.point import Point

from rideshare.geography.projection_transformer import ProjectionTransformer


class GeoPoint(Point):
    """ Simple point representation, which can calculate the distance to another point """

    def __init__(self, lat, lng, projection_transformer=ProjectionTransformer()):
        """
        :param projection_transformer:
        :param lat: latitude
        :param lng: longitude
        :return: Point at lat, lng with projection
        """
        self.equatorial_radius = 6378137.0
        self.lat = float(lat)
        self.lng = float(lng)

        self.x, self.y = projection_transformer.from_gps(lat, lng)

    def translate_meters(self, distance_east, distance_north):
        """
        See http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
        """
        # Earth's equatorial and polar radii
        Rx = self.equatorial_radius
        Ry = 6356752.0

        # Coordinate offsets in radians
        delta_lat = distance_north / Ry
        delta_lng = distance_east / (Rx * math.cos(math.pi * self.lat / 180))

        # Offset position, decimal degrees
        lat = self.lat + delta_lat * 180 / math.pi
        lng = self.lng + delta_lng * 180 / math.pi

        return GeoPoint(lat, lng)

    def fuzz(self, num_points=8, radius=100):
        """
        :rtype: list[GeoPoint]
        """
        points = []
        for i in range(num_points):
            points.append(self.point_on_circumference(radius, i, num_points))
        return points

    def point_on_circumference(self, radius, current_point, total_points):
        """
        :type self: GeoPoint
        :type radius: int
        :type current_point: int
        :type total_points: int
        :return:
        """
        theta = ((math.pi * 2) / total_points)
        angle = (theta * current_point)

        pivot_x = (radius * math.cos(angle))
        pivot_y = (radius * math.sin(angle))

        return self.translate_meters(pivot_x, pivot_y)

    def __str__(self):
        lat_lng = "%s,%s" % (self.lat, self.lng)
        return lat_lng

    def __repr__(self):
        return "Point{%s}" % (str(self))

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False

        return other.distance_to(self) <= 0.00001

    def __ne__(self, other):
        return not (self == other)

    @staticmethod
    def json_load(inp):
        def parse_geopoint(dct):
            if 'lat' in dct:
                return GeoPoint(dct['lat'], dct['lng'])
            return dct

        if isinstance(inp, str):
            return json.loads(inp, object_hook=parse_geopoint)
        else:
            return json.load(inp, object_hook=parse_geopoint)

    @staticmethod
    def json_dump(o):
        class PointEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, GeoPoint):
                    return {'lat': obj.lat, 'lng': obj.lng}
                return json.JSONEncoder.default(self, obj)

        return json.dumps(o, cls=PointEncoder)

    def latlng_distance_to(self, other):
        lat1 = self.lat
        lat2 = other.lat
        lon1 = self.lng
        lon2 = other.lng

        # metres
        y_1 = lat1 * math.pi / 180
        y_2 = lat2 * math.pi / 180
        delta_y = (lat2 - lat1) * math.pi / 180
        delta_x = (lon2 - lon1) * math.pi / 180

        a = math.cos(y_1) * math.cos(y_2) * math.sin(delta_x / 2) * math.sin(delta_x / 2)
        b = math.sin(delta_y / 2) * math.sin(delta_y / 2) + a
        c = 2 * math.atan2(math.sqrt(b), math.sqrt(1 - b))

        return self.equatorial_radius * c


class GeoPointXY(GeoPoint):
    def __init__(self, x, y, projection_transformer=ProjectionTransformer()):
        self.lat, self.lng = projection_transformer.to_gps(y, x)

        Point.__init__(self, x, y)
