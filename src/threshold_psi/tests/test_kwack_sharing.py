import gmpy2
import pytest
from matplotlib import pyplot as plt
from matplotlib.pyplot import savefig

from threshold_psi.kwack_sharing import mk_point, KwackSharing, gen_masks
from threshold_psi.polynomials import lagrange_eval


def plot_path(path, line_style='-', clear=True, save_as=''):
    """
    :type line_style: str
    :type clear: bool
    :type save_as: str
    """
    line, = plt.plot([p[0] for p in path], [p[1] for p in path], line_style)

    if save_as:
        savefig(save_as)

    if clear:
        plt.close()

    return line


def int_to_bits(num, length=None):
    bits = []

    if length:
        max_bit = length
    else:
        max_bit = 1
        while 2 ** max_bit <= num:
            max_bit += 1

    for i in range(max_bit):
        ii = max_bit - i - 1
        if num >= 2 ** ii:
            bits = [1] + bits
            num -= 2 ** ii
        else:
            bits = [0] + bits

    bits.reverse()
    return bits


def mkinp(x):
    bits = int_to_bits(x, length=10)
    first_half = bits[0:len(bits) // 2]
    second_half = bits[len(bits) // 2:]

    return ["".join([str(bit) for bit in half]) for half in [first_half, second_half]]


@pytest.mark.parametrize("expected_x_part, expected_y_part", [mkinp(x) for x in range(0, 2 ** 10 - 1)])
def test_mk_point_1(expected_x_part, expected_y_part):
    mask = int(expected_x_part + expected_y_part, 2)

    actual_x_part, actual_y_part = mk_point(mask, 1613)

    assert int(expected_x_part, 2) == actual_x_part
    assert int(expected_y_part, 2) == actual_y_part

@pytest.mark.parametrize("set_size, t", [(2500, 1250)])
def test_full_kwack_share_protocol(set_size, t):
    # The prime to use for the field
    prime = gmpy2.next_prime(2**128)

    # just 10 random masks
    sender_masks = gen_masks(set_size)

    # Receiver shares  the first t masks
    receiver_masks = sender_masks[:t] + gen_masks(set_size - t)

    # Create the 'kwack'-shares
    kwack = KwackSharing(t, sender_masks, prime)
    hint = kwack.gen_hints()

    # Receiver checks all possible secrets, and sees if any of them resuts in the encrypted zero
    for i in range(set_size - t):
        print "And now i is: %s" % i
        random_masks = hint[0]
        zero = hint[1]
        points = [mk_point(m, prime) for m in receiver_masks[i:i + t]] + random_masks
        if any([p in [pp for pp in points if pp != p] for p in points]):
            raise ValueError
        evaled = lagrange_eval(points, prime, 0)

        found_secret = D(evaled, zero) == 0
        if found_secret:
            print "Intersection is (at least) the items for masks %s-%s" % (i, i + t)
            return

    assert False



# Dummy encryption
def E(s, p):
    return p + s


def D(s, c):
    return c - s
