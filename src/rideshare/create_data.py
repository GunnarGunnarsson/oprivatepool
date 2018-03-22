import argparse

from rideshare.geography.path.google_map_path import GooglePolylinePathEngine, GoogleStepPathEngine
from rideshare.geography.path.here_map_path import HerePathEngine
from rideshare.geography.path.osm_engine import OSMPathEngine
from rideshare.helper.path_data import find_paths

parser = argparse.ArgumentParser(description='Create path data from origin-destination input')
parser.add_argument('alice_origin', type=str, help="Alice's origin, e.g. 'Gothenburg Central Station'")
parser.add_argument('alice_destination', type=str, help="Alice's destination, e.g. 'Stockholm Central Station'")

parser.add_argument('bob_origin', type=str, help="Bob's origin, e.g. 'Halmstad Central Station'")
parser.add_argument('bob_destination', type=str, help="Bob's destination, e.g. 'Uppsala Central Station'")

parser.add_argument('--out', type=str, help="Output folder", default='out')
parser.add_argument('--engine', type=str, help="Map engine to use", default='google_polyline')

args = parser.parse_args()


def main():
    if args.engine == 'google_polyline':
        engine = GooglePolylinePathEngine()
    elif args.engine == 'google_step':
        engine = GoogleStepPathEngine()
    elif args.engine == 'heremaps':
        engine = HerePathEngine()
    elif args.engine == 'OSM':
        engine = OSMPathEngine()
    else:
        raise ValueError('no valid point engine specified')

    find_paths(args.alice_destination.decode('utf-8'), args.alice_origin.decode('utf-8'),
               args.bob_destination.decode('utf-8'), args.bob_origin.decode('utf-8'),
               args.out, engine)


if __name__ == '__main__':
    main()
