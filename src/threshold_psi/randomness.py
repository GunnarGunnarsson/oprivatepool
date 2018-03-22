import random


class RandomSource(object):
    def get_rand(self):
        raise NotImplementedError


class SecureRandomness(RandomSource):
    K = 80

    def get_rand(self):
        #return random.uniform(0, 1)
        return random.randint(0, 2 ** self.K)