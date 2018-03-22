# -*- coding: utf-8 -*-

import itertools

import pytest

from rideshare.geography.path.tests import places, map_paths

routes = list(itertools.permutations(places, 2))

combinations_ = [[(route[0], route[1], name, engine) for name, engine in map_paths] for route in routes]
combinations = [item for sublist in combinations_ for item in sublist]


@pytest.mark.parametrize("origin, destination, path_engine_name, map_path", combinations)
def test_geocode(origin, destination, path_engine_name, map_path):
    path = map_path.path_between(origin, destination)
    assert path is not None
    assert path != []
