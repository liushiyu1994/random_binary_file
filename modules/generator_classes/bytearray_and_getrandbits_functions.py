from ..packages import random


class CurrentGenerator(object):
    """
    This is a little better solution, enough for light use.
    """
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def random_binary_stream(binary_length):
        return bytearray(random.getrandbits(8) for _ in range(binary_length))
