# coding=utf-8
import os

from rideshare.geography.path.client.osm_client import OSMClient
from rideshare.geography.path.client.osm_request import OSMMapAreaRequest
from rideshare.geography.path.client.tests import geocode_place
from rideshare.geography.path.tests import *
from rideshare.helper.util import make_absolute_path_to

client = OSMClient()


def test_download_small_map_by_area():
    loc1 = geocode_place(places[WORK])
    loc2 = geocode_place(places[LINDHOLMEN])
    area_request = OSMMapAreaRequest(loc1, loc2)

    client.execute_area_request(area_request)

    request_successful(area_request)


def test_download_medium_map_by_area():
    loc1 = geocode_place(places[LINDOME])
    loc2 = geocode_place(places[LISEBERG])
    area_request = OSMMapAreaRequest(loc1, loc2)

    client.execute_area_request(area_request)

    request_successful(area_request)


def test_download_large_map_by_area():
    loc1 = geocode_place(places[GOTEBORG])
    loc2 = geocode_place(places[STOCKHOLM])
    area_request = OSMMapAreaRequest(loc1, loc2)

    client.execute_area_request(area_request)

    request_successful(area_request)


def test_download_huge_map_by_area():
    loc1 = geocode_place(places[MALMO])
    loc2 = geocode_place(places[UPPSALA])
    area_request = OSMMapAreaRequest(loc1, loc2)

    client.execute_area_request(area_request)

    request_successful(area_request)


def test_download_extra_huge_map_by_area():
    loc1 = geocode_place(places[MALMO])
    loc2 = geocode_place(places[VEMDALEN])
    area_request = OSMMapAreaRequest(loc1, loc2)

    client.execute_area_request(area_request)

    request_successful(area_request)


def disabled_test_download_map_data_for_europe():
    client.download_europe()
    cached_file_has_entries('europe_full')


def disabled_test_download_map_data_for_sweden():
    client.download_sweden()
    cached_file_has_entries('sweden_full')


def request_successful(request):
    """
    :type url: OSMMapAreaRequest
    """
    for url in [request.make_url(box) for box in request.boxes]:
        cached_file_has_entries(url)


def cached_file_has_entries(url):
    """
    :type url: str
    """
    path = make_absolute_path_to(client.raw_osm_path(url))
    assert os.path.isfile(path)
    with open(make_absolute_path_to(path)) as f:
        lines = f.readlines()
        assert len(lines) > 20


def test_create_database():
    client.create_database()


def disabled_test_find_route_short_medium():  # Doesn't work with shortest path, only quickest
    work = geocode_place(places[WORK])
    lindholmen = geocode_place(places[LINDHOLMEN])
    kallered = geocode_place(places[KALLERED])

    path1 = client.find_route(work, lindholmen)
    path2 = client.find_route(kallered, lindholmen)

    assert len(path1.legs) > 50
    assert len(path2.legs) > 50

    assert len(intersection(path1, path2)) > 40


def test_find_route_large():
    gbg = geocode_place(places[GOTEBORG])
    sthlm = geocode_place(places[STOCKHOLM])

    path1 = client.find_route(gbg, sthlm)

    assert len(path1.legs) > 80


def test_find_route_huge():
    malmoe = geocode_place(places[MALMO])
    uppsala = geocode_place(places[UPPSALA])

    path1 = client.find_route(malmoe, uppsala)

    assert len(path1.legs) > 80


def test_find_route_tricky():
    place1 = geocode_place(places[HJALMARED], client)
    place2 = geocode_place(places[ALINGSAS], client)
    sthlm = geocode_place(places[STOCKHOLM], client)

    path1 = client.find_route(place1, sthlm)
    path2 = client.find_route(place2, sthlm)

    assert len(path1.legs) > 2000
    assert len(path2.legs) > 2000

    assert len(intersection(path1, path2)) < 250


def intersection(path1, path2):
    return set(longlats(path1)).intersection(longlats(path2))


def longlats(path):
    return [(pt.latitude, pt.longitude) for pt in path.legs]
