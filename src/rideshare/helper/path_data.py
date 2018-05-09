import csv
import os
import time

from rideshare.helper.map_plotter import plot_path
from rideshare.helper.util import make_absolute_path_to, create_path

# Generate and print pictures of paths between two points
def find_paths(alice_destination, alice_origin, bob_destination, bob_origin, data_folder, engine):
    paths = create_path_data([(alice_origin, alice_destination), (bob_origin, bob_destination)], data_folder, engine)

    # Generate pictures of the routes
    alice_path_points, bob_path_points = paths
    plot_path(alice_path_points, save_as=create_path(data_folder, 'alice.png'), path_names=['a'])
    plot_path(bob_path_points, save_as=create_path(data_folder, 'bob.png'), path_names=['b'])
    plot_path(bob_path_points, alice_path_points, save_as=create_path(data_folder, 'full.png'), path_names=['b', 'a'])

    return alice_path_points, bob_path_points

# Generate and export intermediate datapoints
def create_path_data(trips, data_folder, engine):
    paths = create_paths(engine, trips)
    return create_data_from_path(paths, data_folder, engine)

# Generate intermediate coordinates
def create_paths(engine, trips):
    paths = []
    for t in trips:
        try:
            print "Searching for path between %s, " % (t,)
            path = engine.map_path.path_between(*t)
            paths.append(path)
        except ValueError, e:
            print "Error searching for path between %s" % (t,)
            print e
    return paths

# Export all intermediate coordinates to CSV
def create_data_from_path(paths, data_folder, engine):
    # MARK
    # Estimated time it takes to traverse one segment in seconds
    est_traveltime = 8
    origin_time = int(time.time())
    
    path_points = [engine.get_points(p, origin_time, str(int(origin_time + (est_traveltime * len(p.legs))))) for idx, p in enumerate(paths)]

    abs_data_path = make_absolute_path_to(data_folder)
    if not os.path.isdir(abs_data_path):
        os.makedirs(abs_data_path)

    with open(create_path(data_folder, 'data.csv'), 'wb') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter='|', quoting=csv.QUOTE_MINIMAL)
        for points in path_points:
            temporal_points = []
            for point in points:
                temporal_points.append("%s, %s, %s" % (point.lat, point.lng, point.time))
            csv_writer.writerow(temporal_points)
    return path_points
