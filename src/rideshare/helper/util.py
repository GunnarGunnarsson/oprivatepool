import csv
import os

from rideshare.geography.geopoint import GeoPoint


def ensure_dir_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def make_absolute_path_to(x):
    if x[0] == '/':
        return x
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', x))


def load_csv_data(folder_or_file):
    """
    :param folder_or_file:
    :rtype: list[list[GeoPoint]]
    """
    paths = []
    if folder_or_file[-4:] == '.csv':
        path = folder_or_file
    else:
        path = create_path(folder_or_file, 'data.csv')
    with open(path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|')
        for row in spamreader:
            # print '|'.join(row)
            paths.append([GeoPoint(*p.split(',')) for p in row])
    return paths


def create_path(folder, image_name):
    return make_absolute_path_to('%s/%s' % (folder, image_name))


def to_point_list(coordinate_intersection, reference_path):
    points = []
    for point in reference_path:
        if (point.lat, point.lng) in coordinate_intersection:
            points.append(GeoPoint(point.lat, point.lng))
    return points


def to_coordinate_set(path):
    return set([(p.lat, p.lng) for p in path])
