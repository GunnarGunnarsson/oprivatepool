import glob
import time
from math import ceil

from rideshare.geography.geopoint import GeoPoint
from rideshare.helper.map_plotter import plot_path
from rideshare.helper.util import make_absolute_path_to
from taxi import config


def main():
    data_folder = make_absolute_path_to(config['data_folder'])
    r = config['r']
    t = config['t']

    for file_name in glob.glob(config['data_filename_pattern'] % data_folder):
        print "\n%s" % file_name
        with open(file_name, 'r') as f:
            paths = GeoPoint.json_load(f)

            count = count_bruteforce(paths, r, t, debug=True)

            print count, 'ridesharing opportunities where found for %s' % file_name


def dynamic_r(base_r, length, x):
    a = (4.0 * base_r) / length ** 2
    b = -(4.0 * base_r) / length
    c = base_r

    return int(a * x ** 2 + b * x + c)


def count_bruteforce(paths, r, threshold, time_max, debug=False):
    count = 0
    ts = {}
    tsc = {}

    def tick(label, t):
        ts[label] = ts.get(label, 0) + time.time() - t
        tsc[label] = tsc.get(label, 0) + 1
        return time.time()

    def stamps():
        if not ts:
            return

        print '-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- '
        for label in ts.keys():
            print '%20s\t%.6f s\t%.6f s\t%s invocations' % (label, ts[label] / tsc[label], ts[label], tsc[label])
        print '-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- '

    for driver_path_index in range(len(paths)):
        # t = time.time()
        driver_path = paths[driver_path_index]
        # tick('driver_path_index', t)

        # print "%s/%s, (%.2f%%)" % (driver_path_index, tot_size, 100 * float(driver_path_index) / tot_size)
        # stamps()
        for passenger_path_index in range(len(paths)):
            if driver_path_index == passenger_path_index:
                continue

            # t = time.time()
            passenger_path = paths[passenger_path_index]
            # t = tick('passenger_path_index', t)

            driver_start = False
            passenger_start = False
            driver_end = False
            passenger_end = False
            min_share_length = int(ceil(len(passenger_path) * threshold))
            if min_share_length < 2:
                continue

            # For every point along the driver's path
            for j in range(len(driver_path)):
                driver_pt = driver_path[j]
                # We compare it to each point along all possible points along the passenger's path
                for i in range(len(passenger_path) - min_share_length + 1):
                    passenger_pt = passenger_path[i]
                    # if the two points are closer than the current r and their times are close enough together
                    current_r = dynamic_r(r, len(passenger_path), i)
                    if driver_pt.distance_to(passenger_pt) < current_r and abs(driver_pt.time - passenger_pt.time) < time_max:
                        print driver_pt.distance_to(passenger_pt), current_r
                        driver_start = j
                        passenger_start = i
                        break

                if passenger_start is not False:
                    break
            # t = tick('driver_path_loop', t)

            if passenger_start is False:
                continue

            for i in reversed(range(passenger_start + min_share_length - 1, len(passenger_path))):
                passenger_pt = passenger_path[i]
                for j in reversed(range(driver_start, len(driver_path))):
                    driver_pt = driver_path[j]
                    current_r = dynamic_r(r, len(passenger_path), i)
                    # Check if there exists another set of points such that
                    # the next two points are closer than r in space and closer than time_max in time
                    if driver_pt.distance_to(passenger_pt) < current_r and abs(driver_pt.time - passenger_pt.time) < time_max:  
                        driver_end = j
                        passenger_end = i
                        break

                if passenger_end is not False:
                    break
            # t = tick('passenger_path_loop', t)

            # If more than one point on b's path is close to the driver's path
            if passenger_start is not False and passenger_end is not False and passenger_start != passenger_end:
                # if the overlap is greater than t
                overlap = passenger_end - passenger_start
                if overlap > min_share_length:
                    count += 1

                    if debug:
                        print "%s can ride with %s [%s -> %s]" % (
                            passenger_path_index, driver_path_index, driver_start, driver_end)
                        # tick('if_statement', t)
    return count


if __name__ == '__main__':
    main()
