import pyproj


class ProjectionTransformer(object):
    # GOOGLE_PROJECTION = pyproj.Proj("+proj=merc +lon_0=0 +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
    GOOGLE_PROJECTION = pyproj.Proj(
        "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +units=m +k=1.0 +nadgrids=@null +no_defs")
    MAPBOX_PROJECTION = pyproj.Proj(
        "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs")

    def __init__(self, projection=None, scale=None):
        super(ProjectionTransformer, self).__init__()

        self.scale = scale or 1
        self.projection = projection or self.GOOGLE_PROJECTION

    def from_gps(self, lat, lng):
        yx = self.projection(lat, lng)
        return reversed([i * self.scale for i in yx])

    def to_gps(self, x, y):
        latlng = self.projection(x, y, inverse=True)
        return latlng

class IntProjectionTransformer(ProjectionTransformer):
    def from_gps(self, lat, lng):
        return [int(x) for x in super(IntProjectionTransformer, self).from_gps(lat, lng)]