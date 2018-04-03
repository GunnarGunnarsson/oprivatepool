import glob
import math
import os
import subprocess
import threading
import time

from protocol.ic_path import ICPath
from rideshare.geography.geopoint import GeoPoint
from rideshare.geography.path.client.osm_client import OSMClient
from rideshare.helper.map_plotter import plot_path
from rideshare.helper.util import load_csv_data, make_absolute_path_to, create_path

BOB_ROLE = 0
ALICE_ROLE = 1


# G
#def set_match_share(path1, path2, threshold):
def set_match_share(path1, path2):
    stash = [{}, {}]

    def run(role):
        run_psi(role, stash)

    alice = lambda: run(ALICE_ROLE)
    bob = lambda: run(BOB_ROLE)

    threads = [threading.Thread(target=user) for user in [alice, bob]]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    for result in stash:
        if result['err']:
            raise ValueError(result['err'])

    if stash[ALICE_ROLE]['out']:
        lines = stash[ALICE_ROLE]['out'].split('\n')
        # G
        #if 'Computation finished. Found' in lines[0]:
        #    result = [GeoPoint(*line.split(',')) for line in lines[1:-1]]
        #    return result
        for idx, l in enumerate(lines):
            if 'Computation finished. Found' in l:
                # G
                result = []
                for line in lines[idx+1:-1]:
                    origin = GeoPoint(line.split(',')[0],line.split(',')[1])
                    if origin not in result:
                        result.append(origin)
                    destination = GeoPoint(line.split(',')[2],line.split(',')[3])
                    if destination not in result:
                        result.append(destination)
                return result

    raise ValueError('Unknown issue')


def setup_psi(path1, path2, threshold):
    def __setup_psi_file(role, trajectory):
        abs_data_path = make_absolute_path_to('psi_input/')
        if not os.path.isdir(abs_data_path):
            os.makedirs(abs_data_path)
        with open(make_data_file_path(role), 'wb') as f:
            # G
            #for point in trajectory:
            for idx, point in enumerate(trajectory):
                try:
                    f.write('%s,%s\n' % (point,trajectory[idx+threshold]))
                except:
                    break

    __setup_psi_file(ALICE_ROLE, path1)
    __setup_psi_file(BOB_ROLE, path2)


def run_psi(role, stash):
    data_file = make_data_file_path(role)
    # G
    # https://github.com/encryptogroup/PSI
    #binary = '/opt/psi/demo'
    # Switched to bark
    binary = '/home/gunnar/Documents/BaRK-OPRF/Release/bOPRFmain.exe'
    protocol = 3
    out, err = _run_psi(binary, data_file, protocol, role)
    # out.output("%s finished with file %s, got \n\tout:%s\n\terr:%s" % (role, data_file, out, err)
    stash[role]['out'] = out
    stash[role]['err'] = err


def make_data_file_path(role):
    directory = make_absolute_path_to('psi_input/')
    data_file = create_path(directory, 'alice.txt' if role == 1 else 'bob.txt')
    return data_file


def _run_psi(binary, data_file, protocol, role):
    # G
    # Switched to fit bark
    #command = '%s -r %s -p %s -f %s' % (
    #    binary, role, protocol, data_file
    #)
    # In bark the roles are switched
    #if role == 0:
    #    bark_role = 1
    #else:
    #    bark_role = 0
    command = '%s -s %s %s' % (
        binary, role, data_file
    )
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    try:
        proc.kill()
    except OSError:
        pass
    return out, err


def endpoint_match_share(path1, path2):
    r = 4
    p = int(20 * 1000 / r)
    ic_path = ICPath(r=r, precision=p)

    match = ic_path.endpoint_match(path1[0], path2[0], path1[-1], path2[-1])

    overlap = path1 if match else []

    return match, overlap


def mix_share(start_match, end_match, si, original_path, threshold):
    if not si:
        return False

    if start_match:
        dist = 0
        last_intersection_index = original_path.index(si[-1])
        for i in range(0, last_intersection_index - 1):
            dist += original_path[i].distance_to(original_path[i + 1])
        if dist > threshold:
            return original_path[:last_intersection_index]

    if end_match:
        dist = 0
        first_intersection_index = original_path.index(si[0])
        for i in range(first_intersection_index, len(original_path) - 1):
            dist += original_path[i].distance_to(original_path[i + 1])
        if dist > threshold:
            return original_path[first_intersection_index:]

    return False


class Output():
    def __init__(self):
        self.__outputs = []

    def output(self, s):
        self.__outputs.append(s)

    @property
    def all_output(self):
        return '\n'.join(self.__outputs)


def dists(path):
    pp = None
    res = []
    for p in path:
        p_ = GeoPoint(p.lat, p.lng)

        if pp is None:
            pp = p_
            continue

        res.append(p_.distance_to(pp))

        pp = p_

    return res


def path_stats(path):
    road_lengths = dists(path)
    return statistics(road_lengths)


def statistics(numbers):
    """
    :type numbers: list[float]
    :rtype: (float, float, float)
    """
    num_roads = len(numbers)
    tot = sum(numbers)
    avg = tot / num_roads
    dev = math.sqrt(sum([(d - avg) ** 2 for d in numbers]) / num_roads)
    return tot, avg, dev


def main():
    # G
    #data_folders = glob.glob(make_absolute_path_to('out/osm/*'))
    data_folders = glob.glob(make_absolute_path_to('damn_out/osm/*'))
    #data_folders = glob.glob(make_absolute_path_to('out/paper/*'))

    for data_folder in data_folders:
        print "\n\n== For %s" % data_folder
        out = Output()

        t = time.time()
        # G
        #threshold = 0.1
        threshold = 1
        alice_path, bob_path = load_csv_data(data_folder)
        out.output(
            "\nLoaded data in %s s. Path lengths are %s and %s" % (time.time() - t, len(alice_path), len(bob_path)))

        stats_format = "tot='%s', avg='%s', std devation='%s'"
        alice_stats = path_stats(alice_path)
        bob_stats = path_stats(bob_path)

        out.output("Section length for Alice num='%s', %s" % (len(alice_path), stats_format % alice_stats))
        out.output("Section length for Bob  num='%s', %s" % (len(bob_path), (stats_format % bob_stats)))
        # print out.all_output
        # continue

        ##
        # Call new PSI function
        ##

        # G
        # setup_psi(alice_path, bob_path)
        setup_psi(alice_path, bob_path, threshold)

        iterations = 25
        times = []
        for i in range(iterations):
            t = time.time()
            # G
            # set_intersection = set_match_share(alice_path, bob_path, threshold)
            set_intersection = set_match_share(alice_path, bob_path)
            times.append(time.time() - t)

        # G
        # fraction_shared = float(len(set_intersection)) / min(len(alice_path), len(bob_path))
        # Fix this
        fraction_shared = float(len(set_intersection)) / min(len(alice_path), len(bob_path))
        # set_match = fraction_shared >= threshold
        set_match = len(set_intersection) > 0

        out.output(
            "Calculated set intersection [%s] (%.2f%% matches)" % (stats_format % statistics(times), 100 * fraction_shared))

        times = []
        for i in range(iterations):
            t = time.time()
            endpoint_match, start_end_overlap = endpoint_match_share(alice_path, bob_path)
            times.append(time.time() - t)

        out.output("Calculated endpoint match [%s]" % (stats_format % statistics(times)))
        out.output("\nSet match: %s" % set_match)
        out.output("Endpoint match %s" % endpoint_match)

        if not set_match:
            set_intersection = []

        plot_for(alice_path, bob_path, get(set_intersection, 0), get(set_intersection, -1),
                 data_folder, 'intersection')
        plot_for(alice_path, bob_path, get(start_end_overlap, 0), get(start_end_overlap, -1), data_folder, 'start_end')

        with open(create_path("%s/paths" % data_folder, 'bench.txt'), 'wb') as f:
            f.write(out.all_output)
            print out.all_output


def get(arr, i):
    return arr[i] if arr else None


def plot_for(alice_path, bob_path, first_point, last_point, data_folder, name):
    intersection = []

    if first_point:
        path = alice_path if first_point in alice_path else bob_path
        i = path.index(first_point)

        while last_point != path[i]:
            intersection.append(path[i])
            i += 1

        intersection.append(path[i])

    plot_path(alice_path, bob_path, intersection, save_as=create_path("%s/paths" % data_folder, '%s.png' % name),
              path_names=['a', 'b', 'i'])


if __name__ == '__main__':
    main()
