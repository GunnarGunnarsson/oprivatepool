from gmpy2 import divm

from numpy.polynomial import Polynomial
from numpy.polynomial.polynomial import polyfit


def evaluate_partial_polynomial(points, d, n, prime):
    secret = 0
    for j in range(len(points)):
        l = divm(n[j], d[j], prime)
        y = points[j][1]
        secret = (secret + y * l) % prime
    return secret


def polynomial_from_points(points, degree):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    approx_coefs = polyfit(xs, ys, degree)
    # coefs = [int(round(c)) for c in approx_coefs]

    polynomial = Polynomial(approx_coefs)
    return polynomial


def lagrange_eval(points, p, x):
    n, d = interpolate_coefficients(p, points, x)

    s = 0
    for j in range(len(points)):
        y = points[j][1]
        s += y * divm(n[j], d[j], p)

    return s % p


def lagrange_secret(points, p):
    n, d = interpolate_coefficients(p, points, 0)
    secret = evaluate_partial_polynomial(points, d, n, p)
    return secret


def lagrange_find_secret(points, hints, t, check, p):
    n, d = interpolate_coefficients(p, points[0:t] + hints, 0)  # O(n^2)

    secret = evaluate_partial_polynomial(points[0:t] + hints, d, n, p)  # O(n)
    if secret == check:
        return 0, t

    set_size = len(points)
    for i in range(1, set_size - t + 1):  # O(n)
        progress_coefficients(points, hints, d, n, i, t, p)

        secret = evaluate_partial_polynomial(points[i:i + t] + hints, d, n, p)
        if secret == check:
            return i, i + t
    return None


def progress_coefficients(points, hints, d, n, i, t, p):
    set_size = len(points)
    n0 = n[0]
    for j in range(t - 1):  # O(n)
        nj = divm(n[j + 1], points[i - 1][0], p)
        nj *= points[i + t - 1][0]
        n[j] = nj
    n[t - 1] = n0

    for j in list(range(t, set_size)):  # O(n)
        nj = divm(n[j], points[i - 1][0], p)
        nj *= points[i + t - 1][0]
        n[j] = nj

    # "normal" denominator rows
    j = 0
    for point in points[i:i + t - 1]:  # O(n)
        goes_away = points[i - 1][0] - point[0]
        new_part = points[i + t - 1][0] - point[0]

        d[j] = d[j + 1] * divm(new_part, goes_away, p)
        j += 1

    # Build new row
    denominator = 1
    for point in points[i:i + t - 1] + hints:  # O(n)
        denominator = denominator * (point[0] - points[i + t - 1][0])
    d[t - 1] = denominator % p

    # Create hint rows
    j = t
    for hint in hints:  # O(n)
        goes_away = points[i - 1][0] - hint[0]
        new_part = points[i + t - 1][0] - hint[0]

        assert (goes_away % p) != 0
        assert (new_part % p) != 0

        d[j] = d[j] * divm(new_part, goes_away, p)
        j += 1

    return n, d


def interpolate_coefficients(p, points, x):
    d = []
    n = []
    for j in range(len(points)):
        numerator = 1
        denominator = 1
        for m in range(len(points)):
            if m == j:
                continue
            xj = points[j][0]
            xm = points[m][0]
            numerator = (numerator * (xm - x))
            denominator = (denominator * (xm - xj))
        n.append(numerator % p)
        d.append(denominator % p)
    return n, d
