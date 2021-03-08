from ..packages import random, itertools


class CurrentGenerator(object):
    """
    This is also faster, better for light use.
    """

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def random_binary_stream(binary_length):
        return bytearray(map(random.getrandbits, itertools.repeat(8, binary_length)))
