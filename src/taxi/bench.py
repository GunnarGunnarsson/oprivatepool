import glob
import sys
import time
from multiprocessing import Pool

from rideshare.geography.geopoint import GeoPoint
from rideshare.helper.util import make_absolute_path_to
from taxi import config
from taxi.bruteforce import count_bruteforce
from taxi.endpoint import count_endpoint
from taxi.intersection import count_intersections


def evaler(i):


    return i[0](i[1][0], i[1][1], i[1][2])


def main():
    rs = [500, 1000, 2000]
    ts = [0.20, 0.50, 0.80]
    finished = [
        '/home/gunnar/Documents/rideshare/taxi-data-10k/complete/routes_green_tripdata_2015-06.json',
        '/home/gunnar/Documents/rideshare/taxi-data-10k/complete/routes_green_tripdata_2015-02.json',
        '/home/gunnar/Documents/rideshare/taxi-data-10k/complete/routes_green_tripdata_2015-10.json',
        '/home/gunnar/Documents/rideshare/taxi-data-10k/complete/routes_green_tripdata_2015-04.json',
        '/home/gunnar/Documents/rideshare/taxi-data-10k/complete/routes_green_tripdata_2015-08.json'
    ]
    data_folder = make_absolute_path_to(config['data_folder'])
    print config['data_filename_pattern'] % data_folder
    for file_name in glob.glob(config['data_filename_pattern'] % data_folder):
        print "\n%s" % file_name
        if file_name in finished:
            continue
        sys.stdout.flush()
        with open(file_name, 'r') as f:
            paths = GeoPoint.json_load(f)

            for r in rs:
                for t in ts:
                    print " ::: [ r=%s, t=%.2f%% ] ::: " % (r, t * 100)
                    sys.stdout.flush()

                    inp = zip([count_bruteforce, count_endpoint, count_intersections], 3 * [(paths, r, t)])

                    p = Pool(5)

                    tt = time.time()
                    mapped = p.map_async(evaler, inp).get(9999999999)

                    print "T=%.6f" % (time.time() - tt)
                    print "\n".join(["%s: %s" % (a, b) for a, b in zip(["BF", "EP", "IS"], mapped)])
        break

if __name__ == '__main__':
    main()
