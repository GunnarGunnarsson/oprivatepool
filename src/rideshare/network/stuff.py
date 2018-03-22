import os
import time

import requests

from rideshare.helper.util import make_absolute_path_to, ensure_dir_exists


def save_file_at_url(url, filename, processor=None):
    response = open_stream(url)
    save_file(filename, response.iter_content(1024), processor)


def open_stream(url, retries=1):
    response = None

    while retries > 0 and not (response and response.ok):
        response = requests.get(url, stream=True)
        retries -= 1
        if not response.ok:
            time.sleep(2)
            # print "Didn't work: %s" % response.content

    return response


def save_file(filename, iterable, processor=None):
    file_path = make_absolute_path_to(filename)

    dir_name = os.path.dirname(file_path)
    ensure_dir_exists(dir_name)

    if isinstance(iterable, str):
        iterable = [iterable]

    with open(file_path, 'wb') as handle:
        for block in iterable:
            if processor:
                handle.write(processor(block))
            else:
                handle.write(block)
