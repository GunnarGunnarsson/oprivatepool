from numpy import random
from unittest.case import TestCase

from rideshare.geography.path.path_util import reduce_path


class PathUtilTest(TestCase):
    def test_reduce_path_small_2(self):
        self.assertEqual(reduce_path([1, 2, 3], 2), [1, 3])

    def test_reduce_path_small_3(self):
        self.assertEqual(reduce_path([1, 2, 3], 3), [1, 2, 3])

    def test_len_enforced(self):
        for i in range(100):
            path = range(random.randint(10, 200))
            target_len = random.randint(9, len(path))
            self.assertEqual(len(reduce_path(path, target_len)), target_len,
                             "Incorrect for length=%s, path=%s" % (target_len, path))

    def test_regression_1(self):
        """
        AssertionError: Incorrect for length=18,
        path=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
        """
        l = 18
        p = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
        reduced = reduce_path(p, l)
        self.assertEqual(len(reduced), l)
