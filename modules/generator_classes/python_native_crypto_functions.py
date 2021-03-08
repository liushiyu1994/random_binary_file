from ..packages import hashlib
from ..common_functions import random_byte_seed_generator


def random_binary_stream_native(binary_length, hash_length, hash_obj, nulls):
    if binary_length < hash_length:
        hash_obj.update(nulls[:binary_length])
        hash_result = hash_obj.digest()
        return hash_result[:binary_length]
    data = bytearray()
    for _ in range(binary_length // hash_length):
        hash_obj.update(nulls)
        data += hash_obj.digest()
    rest_piece = binary_length % hash_length
    if rest_piece >= 1:
        data += random_binary_stream_native(rest_piece, hash_length, hash_obj, nulls)
    return data


class CurrentGenerator(object):
    """
    This function use native hash functions. It uses random key to encrypts null bytes stream,
    and update the stream for each random binary file.
    """

    def __init__(self, seed_length, *args, **kwargs):
        key = random_byte_seed_generator(seed_length)
        self.hash_obj = hashlib.sha1(key)
        self.hash_length = self.hash_obj.digest_size
        self.nulls = bytearray(self.hash_obj.block_size)

    def random_binary_stream(self, binary_length):
        return random_binary_stream_native(binary_length, self.hash_length, self.hash_obj, self.nulls)
