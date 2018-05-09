import hashlib
import random
import urllib

import geojson
import polyline
from geojson import Feature, FeatureCollection, LineString
from geojson.geometry import Point

from rideshare.geography.geopoint import GeoPoint
from rideshare.geography.path.path_util import reduce_path
from rideshare.network.stuff import open_stream, save_file


def plot_path(*paths, **kwargs):
    """
    :type path: list[GeoPoint]
    :type save_as: str
    """

    save_as = kwargs.get('save_as')
    path_names = kwargs.get('path_names')

    coord_paths = []
    for path in paths:
        coord_paths.append([(p.lat, p.lng) for p in path])

    # if len(coord_paths) == 1:
    #     plot_path_polyline(coord_paths[0], save_as, kwargs.get('position'))
    # else:
    plot_path_geojson(coord_paths, save_as, path_names, kwargs.get('position', 'auto'))


def plot_path_polyline(path, save_as, position='auto'):
    """
    :type paths: list[tuple()]
    :type save_as: str
    """

    # max_points = 450
    # if len(path) > max_points:
    #    path = reduce_path(path, max_points)

    token = 'pk.eyJ1IjoienV0IiwiYSI6ImNpc2l0d2M3ODAwMXEybnBreDlraG40b2sifQ.6_Rny7TalpgR2fwbGA6OEw'

    # strokecolor = 'f44'
    orange = 'ffae51'
    blue = '1d00ff'

    if 'alice' in save_as:
        strokecolor = orange
    else:
        strokecolor = blue

    strokeopacity = '0.7'
    fillcolor = 'fff'
    fillopacity = '0.0'
    polyline_string = polyline.encode(path, 5)
    poly_line = urllib.quote(polyline_string)
    polyline_string = 'path-15+%s-%s+%s-%s(%s)' % (strokecolor, strokeopacity, fillcolor, fillopacity, poly_line)

    url = 'https://api.mapbox.com/v4/mapbox.streets/%s/%s/%sx%s.png?access_token=%s' % (
        polyline_string, position, 1280, 1280, token
    )
    l = len(url)

    response = open_stream(url)
    save_file(save_as, response.content)


def plot_path_geojson(paths, save_as, path_names=None, position='auto'):
    """
    :type paths: list[list[tuple()]]
    :type save_as: str
    """
    reductions = 0

    token = 'pk.eyJ1IjoienV0IiwiYSI6ImNpc2l0d2M3ODAwMXEybnBreDlraG40b2sifQ.6_Rny7TalpgR2fwbGA6OEw'

    l = 5000

    # The limit of the request size(?)
    while l >= 4096:
        # Characteristics of the path being drawn
        features = []

        # Iterate for each entity's path
        for i in range(len(paths)):
            path = paths[i]
            if len(path) == 0:
                continue
            max_points = max(len(path) - reductions, 10)
            print "%s: %s" % (i, max_points)
            # Generate a line between the endpoints, made up of max_points evenly spaced points
            line_string = LineString(reduce_path([(x, y) for (y, x) in path], max_points))
            color = gen_hex_colour_code(None if not path_names else path_names[i])
            feature = Feature(geometry=line_string, properties={
                'stroke': '#%s' % color,
                'stroke-opacity': '0.7',
                'stroke-width': '16'
            })
            features.append(feature)

            properties = make_marker_props(None if not path_names else path_names[i])
            start_marker = Feature(geometry=Point((path[0][1], path[0][0])), properties=properties)
            features.append(start_marker)

        for i in reversed(range(len(paths))):
            path = paths[i]
            properties = make_marker_props(None if not path_names else path_names[i])
            end_marker = Feature(geometry=Point((path[-1][1], path[-1][0])), properties=properties)
            features.append(end_marker)

        # Tidy up the JSON string
        geojson_string = urllib.quote(geojson.dumps(FeatureCollection(features)).replace(' ', ''))

        url = 'https://api.mapbox.com/v4/mapbox.streets/geojson(%s)/%s/%sx%s.png?access_token=%s' % (
            geojson_string, position, 1280, 1280, token
        )

        l = len(url)
        print l
        reductions += 1

    # Make the request
    response = open_stream(url)
    # Save the file
    save_file(save_as, response.content)


def make_marker_props(name):
    color = gen_hex_colour_code(name)
    properties = {
        'marker-color': '#%s' % color
    }
    if name:
        properties['marker-symbol'] = name[0]
    return properties


def gen_hex_colour_code(seed=None):
    orange = 'ffae51'
    blue = '1d00ff'

    if not seed:
        return ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
    else:
        if seed == 'a':
            return orange
        elif seed == 'b':
            return blue

        digest = hashlib.sha1(seed).hexdigest()
        return "%0.2X" % (int(digest, 16) % (256 ** 3))
