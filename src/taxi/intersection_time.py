import glob

from math import ceil

from rideshare.geography.geopoint import GeoPoint
from rideshare.helper.util import make_absolute_path_to
from taxi import config


def main():
    data_folder = make_absolute_path_to(config['data_folder'])
    t = config['t']
    print "%s/small_routes.json" % data_folder
    for file_name in glob.glob(config['data_filename_pattern'] % data_folder):
        print "\n%s" % file_name
        with open(file_name, 'r') as f:
            paths = GeoPoint.json_load(f)

            count = count_intersections(paths, None, t, debug=True)

            print count, 'ridesharing opportunities where found'


def count_intersections(paths, r, threshold, time_max, debug=False):
    count = 0
    for driver_path_index in range(len(paths)):
        driver_path = paths[driver_path_index]
        #[[point.lat] for point in driver_path]
        for passenger_path_index in range(len(paths)):
            if driver_path_index == passenger_path_index:
                continue

            passenger_path = paths[passenger_path_index]

            start = None
            end = None
            min_share_length = int(ceil(len(passenger_path) * threshold))

            for i in range(len(passenger_path) - int(min_share_length) + 1):
                passenger_pt = passenger_path[i]
                try:
                    driver_pt_time = driver_path[driver_path.index(passenger_pt)].time
                    if abs(driver_pt_time - passenger_pt.time) < time_max:
                        start = i
                        break
                except:
                    continue

            if start is None:
                continue

            for i in reversed(range(start + min_share_length - 1, len(passenger_path))):
                passenger_pt = passenger_path[i]
                try:
                    driver_pt_time = driver_path[driver_path.index(passenger_pt)].time
                    if abs(driver_pt_time - passenger_pt.time) < time_max:
                        end = i
                        break
                except:
                    continue

            # If more than one point on b's path is on a's path
            if end and start != end:
                # if the overlap is greater than t
                if end - start > min_share_length:
                    count += 1

                    if debug:
                        print "%s can ride with %s [%s -> %s]" % (passenger_path_index, driver_path_index, start, end)
    return count


if __name__ == '__main__':
    main()
