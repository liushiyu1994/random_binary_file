from ..packages import struct, random, itertools


def random_binary_stream_native(binary_length):
    """
    This function use random.getrandbits to generate unsigned long long int (64bits) and use struct to
    pack them together. To optimize performance, 8000 bytes are generated each time.
    """
    # 'Q' in struct means unsigned long long int
    def _struct8k_pack_into(*args):
        return struct.pack_into("!1000Q", *args)

    # Generate 8000 bytes per time. If smaller than 8000, just simply return the result.
    if binary_length < 8000:
        # Use long long int to optimize efficiency
        long_int_num = (binary_length + 7) // 8
        return struct.pack(
            "!{}Q".format(long_int_num),
            *map(random.getrandbits, itertools.repeat(64, long_int_num))
        )[:binary_length]
    # If larger than 8000, generate 8000 each time until the rest piece less than 8000.
    data = bytearray(binary_length)
    for offset in range(0, binary_length - 7999, 8000):
        _struct8k_pack_into(
            data, offset, *map(random.getrandbits, itertools.repeat(64, 1000)))
    # Generate rest piece.
    rest_piece = binary_length % 8000
    if rest_piece >= 1:
        data[-rest_piece:] = random_binary_stream_native(rest_piece)
    return data


class CurrentGenerator(object):
    """
    This function use random.getrandbits to generate unsigned long long int (64bits) and use struct to
    pack them together. To optimize performance, 8000 bytes are generated each time.
    """

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def random_binary_stream(binary_length):
        return random_binary_stream_native(binary_length)
