from rideshare.geography.geopoint import GeoPoint

from rideshare.geography.projection_transformer import ProjectionTransformer


class PathPoint(GeoPoint):
    def __init__(self, lat, lng, tot_dist, meta=None, projection_transformer=ProjectionTransformer()):
        super(PathPoint, self).__init__(lat, lng, meta, projection_transformer)
        self.tot_dist = tot_dist
