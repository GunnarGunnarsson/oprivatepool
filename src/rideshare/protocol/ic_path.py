from bettertimes.crypto.schemes.elgamal import ElGamal
from bettertimes.crypto.schemes.paillier import Paillier
from bettertimes.crypto.util import BitSizedPRNG
from bettertimes.protocol.multiplication_client import Veil, BlindMultiplyRequest
from hos_protocol.array_scramble import ArrayScramble

from rideshare.geography.geopoint import GeoPoint
from rideshare.geography.projection_transformer import IntProjectionTransformer

pathA = []


class ICPath(object):
    def __init__(self, r=6, precision=1):
        """
        :param r: Radius
        :param precision: precision in meters, default 1
        :return:
        """
        super(ICPath, self).__init__()
        self.precision = precision
        self.r = r

        self.scheme = Paillier()
        self.keys = self.scheme.keygen(1024)

    def paths_intersect(self, path_a, path_b):
        intersection = []
        for point in path_a:
            scaled_point = self.scale(point)
            ic = ArrayScramble(self.r, scaled_point, self.keys, self.scheme)
            intersection.append(self.point_on_path(ic, path_b))

        return intersection

    def point_on_path(self, ic, path):
        for p in path:
            if self.get_proximity(ic, p):
                return True

        return False

    def get_proximity(self, array_scramble, point):
        b1 = self.create_proximity_result(array_scramble, point)
        res = array_scramble.get_proximity(b1)
        return res

    def create_proximity_result(self, array_scramble, point):
        scramble = ArrayScramble(self.r, point, self.keys, self.scheme)
        # Constructs the message Alice sends to Bob
        a1 = array_scramble.create_request()
        # Calculate the distance using the unpacked al list
        b1 = scramble.create_response(*a1)
        return b1

    def simple_proximity(self, p1, p2):
        p1 = self.scale(p1)
        p2 = self.scale(p2)
        array_scramble = ArrayScramble(self.r, p1, self.keys, self.scheme)
        return self.get_proximity(array_scramble, p2)

    def endpoint_match(self, s1, s2, e1, e2):
        s1 = self.scale(s1)
        s2 = self.scale(s2)
        array_scramble1 = ArrayScramble(self.r, s1, self.keys, self.scheme)
        prox1 = self.create_proximity_result(array_scramble1, s2)

        e1 = self.scale(e1)
        e2 = self.scale(e2)
        array_scramble2 = ArrayScramble(self.r, e1, self.keys, self.scheme)
        prox2 = self.create_proximity_result(array_scramble2, e2)

        # 10 Elements in each proximity result, need to multiply them all together
        #
        #                                                    f1
        #                               e1
        #                d1                              d2
        #        c1             c2              c3                c4                c5
        #   b1      b2      b3       b4     b5       b6       b7       b8       b9      b10
        # a1 a2   a3 a4   a5 a6   a7 a8   a9 a10  a11 a12  a13 a14  a15 a16  a17 a18  a19 a20

        prng = BitSizedPRNG(num_bits=10)

        prod1 = prox1[0]
        for p in prox1[1:]:
            prod1 = self.outsourced_multiplication(p, prod1, prng)

        prod2 = prox2[0]
        for p in prox2[1:]:
            prod2 = self.outsourced_multiplication(p, prod2, prng)

        return self.dec(prod1 + prod2) == 0

    def outsourced_multiplication(self, factor1, factor2, prng):
        # By bob
        req = BlindMultiplyRequest(factor1, factor2, prng)
        c1, c2 = req.get_request()

        # By Alice
        product = self.enc(self.dec(c1) * self.dec(c2))

        # By bob again
        result = req.reveal(product)
        return result

    """
    Description:
        Transform point (coordinate) to cartesian coordinates with a given position value.
    """
    def scale(self, point):
        projection_transformer = IntProjectionTransformer(scale=1.0 / self.precision)
        return GeoPoint(point.lat, point.lng, projection_transformer=projection_transformer)

    def enc(self, pt):
        return self.scheme.encrypt(self.keys, pt)

    def dec(self, ct):
        return self.scheme.decrypt(self.keys, ct)
