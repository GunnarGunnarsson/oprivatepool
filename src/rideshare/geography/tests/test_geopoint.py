import pytest

from rideshare.geography.geopoint import GeoPoint
from rideshare.geography.path.tests import places_points, places, LINDHOLMEN, WORK
from rideshare.helper.map_plotter import plot_path

lindholmen = places_points[places[LINDHOLMEN]]  # Lindholmen
work = places_points[places[WORK]]  # Work


@pytest.mark.parametrize("l", range(0, 100))
def test_fuzz_length(l):
    ps = lindholmen.fuzz(num_points=l)
    # if ps:
    #     plot_path(ps, save_as='/tmp/foo.png')  # For manual inspection...

    assert len(ps) == l


def test_fuzz_lindholmen():
    ps = lindholmen.fuzz(radius=100, num_points=8)

    plot_path(ps + [ps[0]], save_as='/tmp/foo.png')  # For smanual inspection...

    assert ps == [GeoPoint(57.71081355,11.9462832887),
                  GeoPoint(57.7114508917,11.9457907503),
                  GeoPoint(57.7117148873,11.9446016575),
                  GeoPoint(57.7114508917,11.9434125647),
                  GeoPoint(57.71081355,11.9429200263),
                  GeoPoint(57.7101762083,11.9434125647),
                  GeoPoint(57.7099122127,11.9446016575),
                  GeoPoint(57.7101762083,11.9457907503)
                  ]

    # 11.954984,57.698551,12.56
