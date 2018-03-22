class MapPath(object):
    def path_between(self, origin, destination):
        """
        :rtype: list[GeoPoint]
        """
        raise NotImplementedError

    def geocode(self, place):
        raise NotImplementedError


class PathEngine(object):
    def get_points(self, result):
        """
        :rtype: list[GeoPoint]
        """
        raise NotImplementedError

    def map_path(self):
        raise NotImplementedError


class PathLeg(object):
    def __init__(self, latitude, longitude, segment_dist, total_dist):
        self.longitude = longitude
        self.total_dist = total_dist
        self.latitude = latitude
        self.segment_dist = segment_dist


class Path(object):
    def __init__(self, dist, duration, legs):
        super(Path, self).__init__()
        self.dist = dist
        self.duration = duration
        self.legs = legs