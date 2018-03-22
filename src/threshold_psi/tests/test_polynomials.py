import pytest
from numpy import random
from numpy.polynomial import Polynomial

from threshold_psi.kwack_sharing import gen_masks, mk_point
from threshold_psi.polynomials import polynomial_from_points, lagrange_secret, lagrange_eval, lagrange_find_secret, \
    interpolate_coefficients, evaluate_partial_polynomial, progress_coefficients
from threshold_psi.randomness import RandomSource, SecureRandomness


def rand1to100():
    return mkrand(range(1, 100))


def mkrand(array_like):
    randoms = list(reversed(array_like))

    class R(RandomSource):
        def get_rand(self):
            return randoms.pop()

    return R()


def random_polynomial(degree, secret, random_source=SecureRandomness()):
    coefficients = [secret]

    for i in range(degree):
        coefficients.append(random_source.get_rand())

    polynomial = Polynomial(coefficients)
    return polynomial


def test_lagrange():
    # From wikipedia: https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing
    points = [(1, 1494), (2, 1942), (3, 2578)]
    secret = lagrange_secret(points, 1613)

    assert secret == 1234


def test_lagrange_with_redundant_points():
    # From wikipedia: https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing
    f = lambda x: 1234 + 166 * x + 94 * x ** 2
    points = [(x, f(x)) for x in range(7)]
    secret = lagrange_secret(points, 1613)

    assert secret == 1234


def test_lagrange_over_field():
    # From wikipedia: https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing
    p = 1613
    f = lambda x: (1234 + 166 * x + 94 * x ** 2) % p
    points = [(x, f(x)) for x in range(7)]
    secret = lagrange_secret(points, p)

    assert secret == 1234


@pytest.mark.parametrize("set_size, t", [(1, 1), (2, 1), (3, 1), (10, 1), (10, 2), (10, 5), (10, 8), (10, 9)])
def test_lagrange_secret_hunt(set_size, t):
    p = 1613

    pointsA = gen_points(set_size, p)
    pointsB = gen_points(set_size - t, p) + pointsA[-t:]

    hints = [(x, lagrange_eval(pointsA, p, x)) for x in range(-1, -(set_size - t) - 1, -1)]
    check = lagrange_eval(pointsA, p, 0)
    assert check == lagrange_eval(pointsB[-t:] + hints, p, 0)

    res = lagrange_find_secret(pointsB, hints, t, check, p)
    assert res is not None

    s, e = res
    assert s == set_size-t and e == set_size


def test_small_coefficent_progress():
    t = 2
    p = 1613

    pointsA = [(2, 3), (3, 2), (5, 4)]
    pointsB = [(1, 4), (2, 3), (3, 2)]

    hints = [(x, lagrange_eval(pointsA, p, x)) for x in range(-1, -t, -1)]
    assert hints[0] == (-1, 14)
    check = lagrange_eval(pointsA, p, 0)

    n, d = interpolate_coefficients(p, pointsB[0:t] + hints, 0)

    assert n == [-2 + p, -1 + p, 2]
    assert d == [-2 + p, 3, 6]
    secret = evaluate_partial_polynomial(pointsB[0:t] + hints, d, n, p)
    progress_coefficients(pointsB, hints, d, n, 1, t, p)

    assert [i % p for i in n] == [-3 + p, -2 + p, 6]
    assert [i % p for i in d] == [-3 + p, 4, 12]
    secret = evaluate_partial_polynomial(pointsB[1:t + 1] + hints, d, n, p)

    assert secret == check


def test_coefficent_progress():
    set_size = 10
    t = 5
    p = 1613

    pointsA = gen_points(set_size, p)
    pointsB = gen_points(2, p) + pointsA[4:4 + t] + gen_points(set_size - t - 2, p)

    hints = [(x, lagrange_eval(pointsA, p, x)) for x in range(-1, -1 - t, -1)]

    n, d = interpolate_coefficients(p, pointsB[0:t] + hints, 0)

    set_size = len(pointsB)
    for i in range(1, set_size - t):  # O(n)
        expected_n, expected_d = interpolate_coefficients(p, pointsB[i:t + i] + hints, 0)
        progress_coefficients(pointsB, hints, d, n, i, t, p)

        assert [ni % p for ni in n] == expected_n
        assert [di % p for di in d] == expected_d


def gen_points(set_size, p):
    return [mk_point(m, p) for m in gen_masks(set_size)]
