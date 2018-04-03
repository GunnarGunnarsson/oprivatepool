#!/usr/bin/env python
import hashlib
import os
import re
import subprocess
import time

from geopy import GoogleV3
from geopy.exc import GeocoderTimedOut

from rideshare.geography.geopoint import GeoPoint
from rideshare.geography.path import PathLeg, Path
from rideshare.geography.path.client.osm_request import OSMMapAreaRequest
from rideshare.helper.util import make_absolute_path_to, ensure_dir_exists
from rideshare.network.stuff import open_stream, save_file


def filter_overpass_for_routino(data):
    lines = data.split('\n')
    lines_filtered = filter(lambda line: '<note>' not in line, lines)

    joined = '\n'.join(lines_filtered)
    date_commented_out = re.sub('<meta osm_base="(.*)"/>', '<!--meta osm_base="\g<1>"/-->', joined)

    return date_commented_out


class OSMConnectivityError(ValueError):
    pass


class OSMClient(object):
    geocode_timer = 0
    EUROPE_URL = 'http://download.geofabrik.de/europe-latest.osm.bz2'
    SWEDEN_URL = 'http://download.geofabrik.de/europe/sweden-latest.osm.bz2'

    DATABASE_DIRECTORY = 'data'
    RAW_DATA_DIRECTORY = 'raw_data'
    MAPDATA_FILENAME = '%s/current_map.osm' % RAW_DATA_DIRECTORY

    # G
    ROUTINO_BIN = '/home/gunnar/Documents/routino-3.2/web/bin/'
    # PROFILE_LOCATION = '/opt/routino-bin/profiles.xml'
    # G
    PROFILE_LOCATION = '/home/gunnar/Documents/routino-3.2/web/data/profiles.xml'
    # G
    # TRANSLATIONS_LOCATION = '/opt/routino-bin/translations.xml'
    TRANSLATIONS_LOCATION = '/home/gunnar/Documents/routino-3.2/web/data/translations.xml'
    # G
    TAGGING_LOCATION = '/home/gunnar/Documents/routino-3.2/web/data/tagging.xml'

    @property
    def MAPDATA_FILENAME_WILDCARD(self):
        return '%s/*.osm' % self.RAW_DATA_DIRECTORY

    def raw_osm_path(self, query):
        return '%s/%s.osm' % (self.RAW_DATA_DIRECTORY, hashlib.sha1(query).hexdigest())

    def is_cached(self, query):
        # TODO: check
        return os.path.isfile(make_absolute_path_to(self.raw_osm_path(query)))

    def __init__(self):
        super(OSMClient, self).__init__()
        # self.geocoder = Nominatim()
        # G
        self.geocoder = GoogleV3(api_key="AIzaSyD07ZVAgUgSQzkY5AFLztsRMUwVFx-LNBY")

    def geocode(self, place):
        max_request_frequence = 0.1
        time_since_last_query = time.time() - self.geocode_timer
        time.sleep(max(0, max_request_frequence - time_since_last_query))

        osm_location = None
        tries = 5
        while osm_location is None:
            try:
                osm_location = self.geocoder.geocode(place)
            except GeocoderTimedOut, e:
                time.sleep(2)
                if tries == 0:
                    raise e
            tries -= 1

        self.geocode_timer = time.time()
        return GeoPoint(osm_location.latitude, osm_location.longitude)

    def execute_area_request(self, request):
        """
        :type request: rideshare.geography.path.client.osm_request.OSMMapAreaRequest
        """
        new_data = False

        for box in request.boxes:
            map_url = request.make_url(*box)
            if self.is_cached(map_url):
                continue
            print "Downloading map at %s..." % map_url
            file_name = self.raw_osm_path(map_url)

            if new_data:
                time.sleep(60)

            # G
            # response = open_stream(map_url)
            response = open_stream(map_url, 20)

            match = re.search('runtime error: (.*)', response.content)
            if match:
                raise OSMConnectivityError("Error downloading map data: %s" % (match.group(1)))

            print "Saving file to %s..." % file_name
            save_file(file_name, response.iter_content(1024), filter_overpass_for_routino)
            print "Done!"
            new_data = True
        return new_data

    def make_area_request(self, loc1, loc2):
        return OSMMapAreaRequest(loc1, loc2)

    def download_europe(self):
        if not self.is_cached('europe_full'):
            response = open_stream(self.EUROPE_URL)
            save_file(make_absolute_path_to(self.raw_osm_path('europe_full')), response.iter_content(1024))

    def download_sweden(self):
        if not self.is_cached('sweden_full'):
            response = open_stream(self.SWEDEN_URL)
            save_file(make_absolute_path_to(self.raw_osm_path('sweden_full')), response.iter_content(1024))

    def create_database(self):
        """
        Only needs to be run once per environment (per 'data' directory)
        """
        data_folder = make_absolute_path_to(self.DATABASE_DIRECTORY)
        ensure_dir_exists(data_folder)

        osm_file_path = make_absolute_path_to(self.MAPDATA_FILENAME_WILDCARD)

        print "Creating database..."

        # G
        command = '%s/planetsplitter --dir="%s" --tagging=%s %s' % (
            self.ROUTINO_BIN, data_folder, self.TAGGING_LOCATION, osm_file_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()

        if err:
            raise ValueError("Couldn't create database from OSM data: %s" % err)

        print "Done!"

    # Generate the intermediate points between the two coordinates, representing a path
    def find_route(self, origin, destination):
        """
        :param origin: start of route
        :param destination: end of route
        :type origin: GeoPoint
        :type destination: GeoPoint
        """

        try:
            if self.execute_area_request(OSMMapAreaRequest(origin, destination)):
                self.create_database()
        except OSMConnectivityError, e:
            print e
            return

        data_folder = make_absolute_path_to(self.DATABASE_DIRECTORY)
        if not os.path.isfile('%s/%s' % (data_folder, 'nodes.mem')):
            self.create_database()

        coords = '--lon1=%s --lat1=%s --lon2=%s --lat2=%s' % (origin.lng, origin.lat, destination.lng, destination.lat)
        # G
        # Initialize the command for Routino, inputing the endpoints coordinates
        command = '%s/router --shortest --output-stdout --output-text-all --profiles=%s --translations=%s --dir=%s %s' % (
            self.ROUTINO_BIN, self.PROFILE_LOCATION, self.TRANSLATIONS_LOCATION, data_folder, coords
        )
        # Run the command
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()

        if err:
            raise ValueError("Unable to find route for ('%s' -> '%s'): %s" % (origin, destination, err))

        # The output is basically CSV with \t delimiter
        cells = [line.split('\t') for line in out.split('\n')[6:-1]]
        legs = [OSMPathLeg(*cell) for cell in cells]

        return Path(legs[-1].total_dist, legs[-1].total_duration, legs)


class FileCache(object):
    def __init__(self, filename):
        self.filename = filename

    def cache(self, data):
        filename = make_absolute_path_to(self.filename)
        save_file(filename, data, filter_overpass_for_routino)


class OSMPathLeg(PathLeg):
    def __init__(self, latitude, longitude, node, node_type, segment_dist, segment_duration, total_dist, total_duration,
                 speed=None, bearing=None, highway=None):
        super(OSMPathLeg, self).__init__(latitude, longitude, segment_dist, total_dist)
        self.node = node
        self.node_type = node_type
        self.segment_duration = segment_duration
        self.total_duration = total_duration
        self.speed = speed
        self.bearing = bearing
        self.highway = highway
