import glob

from rideshare.helper.map_plotter import plot_path
from rideshare.helper.util import load_csv_data, make_absolute_path_to, create_path


def main():
    bay_area_center = '-122.289873,37.651233,11'
    data_folders = glob.glob(make_absolute_path_to('out/paper/*'))

    for data_folder in data_folders:
        print "\n\n== For %s" % data_folder

        datas = load_csv_data(data_folder)
        alice_path, bob_path = datas

        scenario_name = data_folder[data_folder.rindex("/") + 1:]
        # plot_path(alice_path, path_names=["a"], save_as=create_path("paper_figs/%s/" % scenario_name, 'a.png'),#
        #          position=bay_area_center)
        # plot_path(bob_path, path_names=["b"], save_as=create_path("paper_figs/%s/" % scenario_name, 'b.png'),#
        #          position=bay_area_center)
        plot_path(alice_path, bob_path, path_names=["a", "b"],
                  save_as=create_path("paper_figs/%s/" % scenario_name, 'plot.png'),
                  position=bay_area_center)


if __name__ == '__main__':
    main()
