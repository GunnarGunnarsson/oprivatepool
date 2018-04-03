import csv
import os
import random
import sys
import urllib

from rideshare.geography.geopoint import GeoPoint
from rideshare.geography.path.osm_engine import OSMPathEngine
from rideshare.helper.util import make_absolute_path_to, create_path
from taxi.trip import GreenNewTaxiTrip, GreenTaxiTrip


def main():
    data_folder = 'taxi-data-10k'

    abs_data_path = make_absolute_path_to(data_folder)
    if not os.path.isdir(abs_data_path):
        os.makedirs(abs_data_path)

    all_taxi_links_url = 'https://raw.githubusercontent.com/toddwschneider/nyc-taxi-data/master/raw_data_urls.txt'
    str = "[SETUP] fetching urls from %s" % all_taxi_links_url
    print_flushed(str)
    f = urllib.urlopen(all_taxi_links_url)
    all_taxi_links = f.read().split('\n')
    f.close()

    for taxi_link in all_taxi_links:
        # G
        #if 'green_tripdata' not in taxi_link:
        if 'green_tripdata_2015' not in taxi_link:
            continue

        source_name = taxi_link.split('/')[-1]
        target_name = 'routes_%s.json' % source_name[:-4]

        # Only handle every second month
        if int(source_name.split('.')[0].split('-')[1], 10) % 2 != 0:
            continue

        target_completed_file_name = make_absolute_path_to('%s/complete/%s' % (data_folder, target_name))
        if os.path.isfile(target_completed_file_name):
            continue

        target_file_name = create_path(data_folder, target_name)
        source_file = make_absolute_path_to('%s/%s' % (data_folder, source_name))

        if os.path.isfile(source_file):
            # The CSV file is already downloaded
            print_flushed("[CACHED] %s" % taxi_link)
        else:
            print_flushed("[DOWNLOAD] %s" % taxi_link)
            tmp_source_file = "%s_tmp" % source_file
            urllib.urlretrieve(taxi_link, tmp_source_file)
            os.rename(tmp_source_file, source_file)

        lines = len(open(source_file).readlines())

        engine = OSMPathEngine()

        with open(target_file_name, 'wb') as target_file:
            percentage = 5
            target = 1000  # lines / percentage
            target_file.write("[")

            rows = []
            # Read the CSV file
            print_flushed("[READ] %s" % taxi_link)
            with open(source_file, 'rb') as csv_file:
                next(csv_file, None)  # skip the headers

                csv_reader = csv.reader(csv_file)

                for row in csv_reader:
                    rows.append(row)

            count = 0
            print_flushed('[ROUTE] %s' % taxi_link)
            # Look through the first 1000 rows of data in the CSV file
            while count < target and rows:
                current_percentage = 100.0 * count / target

                if current_percentage == round(int(current_percentage)) and current_percentage % 10 == 0:
                    print_flushed('\t%.2f%% routed (%s/%s, total %s)' % (current_percentage, count, target, lines))

                i = random.randint(0, len(rows) - 1)
                row = rows.pop(i)

                try:
                    if GreenNewTaxiTrip.is_new_link(taxi_link):
                        trip = GreenNewTaxiTrip(*row)
                    else:
                        trip = GreenTaxiTrip(*row)
                except TypeError, e:
                    original_lines = open(source_file).readlines()
                    err_line_number = '?'  # original_lines.index(",".join(row))
                    print_flushed("Could not handle line #%s. %s" % (err_line_number, e))
                if '0' not in [trip.pickup_latitude, trip.pickup_longitude, trip.dropoff_latitude,
                               trip.dropoff_longitude]:
                    dropoff = (trip.dropoff_latitude, trip.dropoff_longitude)
                    pickup = (trip.pickup_latitude, trip.pickup_longitude)
                    try:
                        # print "Searching for path for [%s -> %s]\n\t%s" % (pickup, dropoff, row)
                        # Create points from the given coordinates
                        pickup_point = GeoPoint(*pickup)
                        dropoff_point = GeoPoint(*dropoff)
                        if pickup_point.distance_to(dropoff_point) < 2000:
                            continue
                        # Generate the path between the two points
                        path = engine.map_path.path_between(pickup_point, dropoff_point)
                        points = engine.get_points(path)
                        if len(points) < 10:
                            continue

                        json_dump = GeoPoint.json_dump(points)
                        if count > 0:
                            target_file.write(",")
                        target_file.write(json_dump)
                        count += 1
                    except ValueError, e:
                        print_flushed("Error searching for path for [%s -> %s]. %s" % (pickup, dropoff, e))

            target_file.write("]")
        print_flushed('\t%.2f%% rout    ed (%s/%s, total %s)' % (100.0 * count / target, count, target, lines))

        os.rename(source_file, make_absolute_path_to('%s/complete/%s' % (data_folder, source_name)))
        os.rename(target_file_name, target_completed_file_name)

        print_flushed("[DONE] %s" % taxi_link)


def print_flushed(str):
    print str
    sys.stdout.flush()


if __name__ == '__main__':
    main()
