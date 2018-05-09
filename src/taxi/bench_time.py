import glob
import sys
import time
from multiprocessing import Pool

from rideshare.geography.geopoint import GeoPoint
from rideshare.helper.util import make_absolute_path_to
from taxi import config
from taxi.bruteforce_time import count_bruteforce
from taxi.endpoint_time import count_endpoint
from taxi.intersection_time import count_intersections


def evaler(i):
    # i[0] is the function to-be-run
    # i[1][0] is the list of coordinates along the path
    # i[1][1] is the spatial deviance value
    # i[1][2] is the threshold value
    # i[1][3] is the temporal deviance value
    return i[0](i[1][0], i[1][1], i[1][2], i[1][3])

def main():
    # spatial deviance (radius)
    rs = [500, 1000, 2000]
    # thresholds
    ts = [0.20, 0.50, 0.80]
    # temporal deviance (distance)
    ds = [1800, 2700, 3600]

    data_folder = make_absolute_path_to(config['data_folder'])
    print config['data_filename_pattern'] % data_folder
    for file_name in glob.glob(config['data_filename_pattern'] % data_folder):
        print file_name
        sys.stdout.flush()
        with open(file_name, 'r') as f:
            paths = GeoPoint.json_load(f)

            for r in rs:
                for t in ts:
                    for d in ds:
                        print " ::: [ r=%s, t=%.2f%%, d=%d ] ::: " % (r, t * 100, d/60)
                        sys.stdout.flush()

                        inp = zip([count_bruteforce, count_endpoint, count_intersections], 3 * [(paths, r, t, d)])

                        p = Pool(1)

                        tt = time.time()
                        mapped = p.map_async(evaler, inp).get(9999999999)

                        print "T=%.6f" % (time.time() - tt)
                        print "\n".join(["%s: %s" % (a, b) for a, b in zip(["BF", "EP", "IS"], mapped)])

if __name__ == '__main__':
    main()
