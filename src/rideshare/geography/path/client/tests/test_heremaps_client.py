from unittest.case import TestCase

import configparser

from rideshare.geography.path.client.heremaps_client import HereMapsClient
from rideshare.geography.path.tests import places, GOTEBORG, STOCKHOLM
from rideshare.helper.util import make_absolute_path_to


class TestHereMapsClient(TestCase):
    def test_geocode(self):
        search = "Berlin"

        settings = configparser.ConfigParser()

        settings.read(make_absolute_path_to('config/settings.cfg'))
        app_id = settings.get('HERE', 'app_id')
        app_code = settings.get('HERE', 'app_code')
        client = HereMapsClient(app_id, app_code)

        result = client.geocode(search)
        self.assertEqual(str(result)[0:4], 'geo!')
        self.assertTrue(len(str(result)) > 10)

    def test_route(self):
        start = places[GOTEBORG]
        finish = places[STOCKHOLM]

        settings = configparser.ConfigParser()
        settings.read(make_absolute_path_to('config/settings.cfg'))
        app_id = settings.get('HERE', 'app_id')
        app_code = settings.get('HERE', 'app_code')
        client = HereMapsClient(app_id, app_code)

        origin = client.geocode(start)
        destination = client.geocode(finish)

        result = client.route(origin, destination)
        steps = result['leg'][0]['maneuver']

        lnglat_ = [s['position'] for s in steps]
        lnglat = [(s['latitude'], s['longitude']) for s in lnglat_]
        self.assertEqual(len(lnglat), 20)
