def reduce_path(path, max_points=100):
    """
    Keeps the first and last point in the path, and chooses `max_points-2` evenly spaced points in between

    References
        http://stackoverflow.com/questions/9873626/choose-m-evenly-spaced-elements-from-a-sequence-of-length-n
        https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm

    :param path:
    :param max_points:
    :return:
    """
    assert max_points >= 2

    if len(path) <= max_points:
        return path

    first = path[0]
    del path[0]
    last = path[-1]
    del path[-1]

    max_points -= 2

    l = len(path)

    indexes = [i * l // max_points + l // (2 * max_points) for i in range(max_points)]

    result = [first]

    for i in indexes:
        result.append(path[i])
    result.append(last)
    return result
