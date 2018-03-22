# -*- coding: utf-8 -*-

import pytest

from rideshare.geography.path.tests import map_paths, places

combinations_ = [[(place, name, engine) for name, engine in map_paths] for place in places]
combinations = [item for sublist in combinations_ for item in sublist]


@pytest.mark.parametrize("place, path_engine_name, path_engine", combinations)
def test_geocode(place, path_engine_name, path_engine):
    path = path_engine.geocode(place)
    assert path is not None
    assert path != []
