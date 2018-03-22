import random

from threshold_psi.polynomials import lagrange_eval

MASK_SIZE = 10


def mk_point(m, p):
    y_part = m & (2 ** (MASK_SIZE // 2) - 1)
    return m % p, y_part % p


class KwackSharing(object):
    def __init__(self, threshold, masks, prime):
        super(KwackSharing, self).__init__()
        self.k = threshold
        self.masks = masks
        self.prime = prime

    def gen_hints(self):
        hint_size = len(self.masks) - self.k
        random_masks = gen_masks(hint_size)
        secret_hint = self.interpolate_for_x(0)
        hint_points = [(-m, self.interpolate_for_x(-m)) for m in random_masks]
        return hint_points, secret_hint

    def interpolate_for_x(self, x):
        return lagrange_eval([mk_point(m, self.prime) for m in self.masks], self.prime, x)


def gen_masks(num_masks):
    # Just creates random bitstrings to act as masks
    masks = []
    for i in range(num_masks):
        bits = random.getrandbits(128)
        masks.append(bits)
    return masks
