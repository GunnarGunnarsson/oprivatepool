import hashlib

from rideshare.helper.map_plotter import plot_path
from rideshare.helper.util import make_absolute_path_to, load_csv_data


def main():
    NYC = '-73.99,40.70,12'

    data_folder = make_absolute_path_to('taxi-data')

    paths = load_csv_data(data_folder)

    a = paths[49]
    b = paths[55]

    for path in paths:
        i = paths.index(path)
        plot_path(path, save_as='/tmp/taxiplots/%s.png' % paths.index(path), position=NYC)  # For manual inspection...


if __name__ == '__main__':
    main()
