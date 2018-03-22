from rideshare.geography.geopoint import GeoPoint
from rideshare.geography.path.here_map_path import HerePathEngine, HereMapPath
from rideshare.geography.path.tests import places

extractor = HerePathEngine()


def test_empty_gives_empty():
    assert extractor.get_points({'leg': []}) == []


def test_nonempty_gives_geopoint():
    route = {'leg': [{'maneuver': [dict(_type=u'PrivateTransportManeuverType', id=u'M1', instruction=u'...', length=24,
                                        position={u'latitude': 52.5160693, u'longitude': 13.376988}, travelTime=18)]}]}
    assert len(extractor.get_points(route)) == 1
    assert isinstance(extractor.get_points(route)[0], GeoPoint)


def test_got_sthml():
    path = HereMapPath().path_between(places[GOTEBORG], places[STOCKHOLM])
    points = extractor.get_points(path)
    assert len(points) > 5
