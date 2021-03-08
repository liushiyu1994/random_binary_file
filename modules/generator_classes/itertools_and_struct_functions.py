from ..packages import struct, random, itertools


class CurrentGenerator(object):
    """
    This function use random.getrandbits to generate unsigned long long int (64bits) and use struct to
    pack them together.
    """

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def random_binary_stream(binary_length):
        # Use long long int to optimize efficiency
        long_int_num = (binary_length + 7) // 8
        return struct.pack(
            "!{}Q".format(long_int_num),
            *map(random.getrandbits, itertools.repeat(64, long_int_num))
        )[:binary_length]