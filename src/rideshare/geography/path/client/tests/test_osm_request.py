import itertools
import pytest

from rideshare.geography.path.client.osm_request import OSMMapAreaRequest
from rideshare.geography.path.client.tests import geocode_place
from rideshare.geography.path.tests import *


def test_flat_area_request():
    """
    Should give boxes for

    lat
    ^
    |
    +-->  long

       8       9       10      11      12     13      14
    10 +-------+-------+-------+-------+------+-------+
       |       |   X   |   X   |   X   |  X   |       |
       |       |       |       |       |      |       |
    11 +-------+-------+-------+-------+------+-------+
       |       |       |       |       |      |       |
       |       |       |       |       |      |       |
    12 +-------+-------+-------+-------+------+-------+

    :param self:
    :return:
    """

    loc1 = GeoPoint(10.3, 10)
    loc2 = GeoPoint(10.5, 12.1)

    req = OSMMapAreaRequest(loc1, loc2)

    assert len(req.boxes) == 4


def test_square_area_request():
    """
    Should give boxes for

    lat
    ^
    |
    +-->  long

       8       9       10      11      12     13      14
    10 +-------+-------+-------+-------+------+-------+
       |       |   X   |   X   |   X   |  X   |       |
       |       |       |       |       |      |       |
    11 +-------+-------+-------+-------+------+-------+
       |       |   X   |   X   |   X   |  X   |       |
       |       |       |       |       |      |       |
    12 +-------+-------+-------+-------+------+-------+
       |       |   X   |   X   |   X   |  X   |       |
       |       |       |       |       |      |       |
    13 +-------+-------+-------+-------+------+-------+
       |       |       |       |       |      |       |
       |       |       |       |       |      |       |
    14 +-------+-------+-------+-------+------+-------+

    :param self:
    :return:
    """

    loc1 = GeoPoint(10.3, 10)
    loc2 = GeoPoint(12.5, 12)

    req = OSMMapAreaRequest(loc1, loc2)

    assert len(req.boxes) == 12


short_medium_routes = [
    (places[LINDOME], places[LISEBERG]),
    (places[KALLERED], places[OLSKROKEN]),
    (places[HOME], places[LINDHOLMEN]),
    (places[WORK], places[LINDHOLMEN])  # lindholmen reused
]


@pytest.mark.parametrize("origin, destination", short_medium_routes)
def test_short_medium(origin, destination):
    loc1 = geocode_place(origin)
    loc2 = geocode_place(destination)

    req = OSMMapAreaRequest(loc1, loc2)

    assert len(req.boxes) == 2

    urls = [req.make_url(*box) for box in req.boxes]
    assert 'http://overpass-api.de/api/map?bbox=10.0,56.0,11.1,57.1' in urls
    assert 'http://overpass-api.de/api/map?bbox=11.0,56.0,12.1,57.1' in urls


large_routes = [
    (places[GOTEBORG], places[STOCKHOLM]),
    (places[MALMO], places[UPPSALA]),
]


@pytest.mark.parametrize("origin, destination", large_routes)
def test_large(origin, destination):
    loc1 = geocode_place(origin)
    loc2 = geocode_place(destination)

    req = OSMMapAreaRequest(loc1, loc2)

    assert len(req.boxes) in [9, 10]


def test_box_collection():
    reqs = []
    for l1, l2 in itertools.product(places, places):
        loc1 = geocode_place(l1)
        loc2 = geocode_place(l2)

        reqs.append(OSMMapAreaRequest(loc1, loc2))

    boxes = set()
    for req in reqs:
        for box in req.boxes:
            boxes.add(box)

    boxes = sorted(sorted(boxes, key=lambda x: x[1]), key=lambda x: x[0])
    assert len(boxes) == 25
