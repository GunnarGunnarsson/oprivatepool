import glob

from rideshare.geography.geopoint import GeoPoint
from rideshare.helper.map_plotter import plot_path
from rideshare.helper.util import make_absolute_path_to, load_csv_data
from taxi import config


def main():
    data_folder = make_absolute_path_to(config['data_folder'])
    r = config['r']

    for file_name in glob.glob(config['data_filename_pattern'] % data_folder):
        print "\n%s" % file_name
        with open(file_name, 'r') as f:
            paths = GeoPoint.json_load(f)

            count = count_endpoint(paths, r, None, debug=True)

            print count, 'ridesharing opportunities where found'


def count_endpoint(paths, r, threshold, time_max, debug=False):
    count = 0
    for driver_path_index in range(len(paths)):
        driver_path = paths[driver_path_index]
        driver_start = driver_path[0]
        driver_end = driver_path[-1]

        for passenger_path_index in range(len(paths)):
            if driver_path_index == passenger_path_index:
                continue

            passenger_path = paths[passenger_path_index]

            passenger_start = passenger_path[0]
            passenger_end = passenger_path[-1]

            start = False
            end = False

            if driver_start.distance_to(passenger_start) < r and abs(driver_start.time - passenger_start.time) < time_max:
                start = driver_start

            if driver_end.distance_to(passenger_end) < r and abs(driver_end.time - passenger_end.time) < time_max:
                end = driver_end

            # If more than one point on b's path is close to a's path
            if start and end:
                count += 1

                if debug:
                    print "%s can ride with %s [%s -> %s]" % (passenger_path_index, driver_path_index, 0, len(passenger_path))

                    filename = '/tmp/taxiplots/endpoint/%s_%s.png' % (driver_path_index, passenger_path_index)

                    plot_path(driver_path, passenger_path,
                              save_as=filename,
                              position=config['ny'],
                              path_names=['driver', 'passenger'])
    return count


if __name__ == '__main__':
    main()
