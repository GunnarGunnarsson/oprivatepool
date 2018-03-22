from rideshare.geography.path.osm_engine import OSMPathEngine
from rideshare.geography.path.tests import *
from rideshare.helper.map_plotter import plot_path, gen_hex_colour_code

path_engine = OSMPathEngine()


def test_plot_simple():
    lindholmen = places[LINDHOLMEN]
    lindholmen_coords = places_points[lindholmen]  # Lindholmen
    work = places[WORK]
    work_coords = places_points[work]  # Work

    plot_path([lindholmen_coords, work_coords], save_as='/tmp/foo.png')  # For manual inspection...


def test_plot_foo():
    lindholmen = places[LINDHOLMEN]
    lindholmen_coords = places_points[lindholmen]  # Lindholmen
    work = places[WORK]
    work_coords = places_points[work]  # Work

    plot_path([lindholmen_coords, places_points[places[HOME]], work_coords],
              save_as='/tmp/foo_3.png')  # For manual inspection...


def test_plot_path():
    lindholmen = places[LINDHOLMEN]
    lindholmen_coords = places_points[lindholmen]  # Lindholmen
    work = places[WORK]
    work_coords = places_points[work]  # Work
    path = path_engine.get_points(path_engine.map_path.path_between(work_coords, lindholmen_coords))

    plot_path(path, save_as='/tmp/foo_path.png')  # For manual inspection...


def test_plot_multi_line():
    lindholmen_coords = places_points[places[LINDHOLMEN]]
    work_coords = places_points[places[WORK]]
    home_coords = places_points[places[HOME]]

    path1 = path_engine.get_points(path_engine.map_path.path_between(work_coords, lindholmen_coords))
    path2 = path_engine.get_points(path_engine.map_path.path_between(home_coords, lindholmen_coords))

    plot_path(path1, path2, save_as='/tmp/foo_multi.png')  # For manual inspection...


def test_plot_huge_path():
    malmo = places_points[places[MALMO]]
    uppsala = places_points[places[UPPSALA]]
    path = path_engine.get_points(path_engine.map_path.path_between(uppsala, malmo))

    plot_path(path, save_as='/tmp/foo_huge.png')  # For manual inspection...


def test_gen_hex_colour_code():
    seed = 'foo'
    col1 = gen_hex_colour_code(seed)
    col2 = gen_hex_colour_code(seed)
    assert col1 == col2
